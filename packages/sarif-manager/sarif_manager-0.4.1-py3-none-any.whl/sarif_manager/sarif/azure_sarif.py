import json
from typing import Union

from sarif_manager.sarif.azure_sarif_finding import AzureSarifFinding
from sarif_manager.sarif.azure_sarif_utils import create_work_item, get_azure_headers, get_azure_work_items_api_url


class AzureSarif:
    def __init__(self):
        self.sarif_data = {}
        self.sarif_findings = []
        self.pat: Union[str, None] = None
        self.azure_headers: Union[dict, None] = None
        self.organization: Union[str, None] = None
        self.project: Union[str, None] = None
        self.repo_url: Union[str, None] = None

    @property
    def azure_api_url(self):
        """Get the Azure DevOps API URL for work items."""
        if not self.organization or not self.project:
            return None
        return get_azure_work_items_api_url(self.organization, self.project)

    def load_from_file(self, sarif_file: str):
        with open(sarif_file, 'r') as file:
            self.sarif_data = json.load(file)
        self.parse()

    def set_metadata(self, organization: str, project: str):
        self.organization = organization
        self.project = project
        self.repo_url = f'https://dev.azure.com/{organization}/_git/{project}'

    def set_auth(self, pat: str):
        self.pat = pat
        # Headers for Azure DevOps API
        self.azure_headers = get_azure_headers(pat)

    def parse(self):
        for run in self.sarif_data.get('runs', []):
            for result in run.get('results', []):
                # fmt: off
                location = result.get('locations', [{}])[0].get('physicalLocation', {}).get('artifactLocation', {}).get('uri')
                line = result.get('locations', [{}])[0].get('physicalLocation', {}).get('region', {}).get('startLine', 0)
                description = "No description available."
                fingerprints = result.get('partialFingerprints', {})

                for rule in run['tool']['driver']['rules']:
                    if rule['id'] == result.get('ruleId'):
                        description = rule['fullDescription']['text']
                        break
                # fmt: on
                finding = {
                    'rule_id': result.get('ruleId'),
                    'message': result.get('message', {}).get('text'),
                    'severity': result.get('level'),
                    'location': location,
                    'line': line,
                    'description': description,
                    'fingerprints': fingerprints
                }
                self.sarif_findings.append(finding)
        return self.sarif_findings

    def azure_devops_messages(self):
        """
        To log the findings in Azure DevOps pipelines as warnings or errors, you need to format the messages as
        Azure DevOps logging commands. This method generates the logging commands for each finding.

        More details: https://learn.microsoft.com/en-us/azure/devops/pipelines/scripts/logging-commands?view=azure-devops&tabs=bash
        """
        messages = set()
        for item in self.sarif_findings:
            item['repo_url'] = self.repo_url
            this_finding = AzureSarifFinding(**item)
            if this_finding.exclude:
                continue
            messages.add(this_finding.azure_devops_message)
        messages = list(messages)
        messages.sort()
        return messages

    def print_logging_commands(self):
        """Print the Azure DevOps logging commands to the console."""
        messages = self.azure_devops_messages()
        for message in messages:
            print(message)

    def create_work_items(self):
        """Create work items in Azure DevOps for each finding."""
        if not self.azure_headers or not self.organization or not self.project:
            raise ValueError("Azure DevOps credentials and metadata must be set before creating work items")

        for item in self.sarif_findings:
            item['repo_url'] = self.repo_url
            this_finding = AzureSarifFinding(**item)
            if this_finding.exclude:
                continue
            
            create_work_item(
                rule_id=this_finding.rule_id,
                issue_title=this_finding.message,
                issue_description=this_finding.description_with_source_code_link(),
                api_url=self.azure_api_url,
                headers=self.azure_headers,
                organization=self.organization,
                project=self.project,
                fingerprints=this_finding.fingerprints
            )
