from sarif_manager.sarif.azure_sarif_utils import trim_uuid


class AzureSarifFinding:
    def __init__(self, repo_url: str, rule_id: str, message: str, severity: str, location: str, line: int, description: str, fingerprints: dict = None):
        self.repo_url = repo_url
        self.original_rule_id = rule_id
        self.rule_id = trim_uuid(rule_id)
        self.message = message
        self.severity = 'warning' if severity == 'warning' else 'error'
        self.location = location
        self.line = line
        self.description = description
        self.fingerprints = fingerprints or {}

    def description_with_source_code_link(self):
        """
        Replace mentions of the `location` in the description with a markdown formatted link to the source code.

        It's enclosed in backticks to make it look like code. We need to replace the backticks as well.
        """
        result = self.description.replace(f"`{self.location}`", f"[{self.location}]({self.file_url})")
        return result

    @property
    def file_path(self):
        """
        Normalize path to always have a leading slash and forward slashes.
        """
        # Replace backslashes with forward slashes
        path = self.location.replace('\\', '/')
        # Ensure single leading slash
        return '/' + path.lstrip('/')

    @property
    def file_url(self):
        """Generate Azure DevOps URL for the file."""
        return f"{self.repo_url}?path={self.file_path}&version=GBmain&line={self.line + 1}&lineEnd={self.line + 2}&lineStartColumn=1&lineEndColumn=1&lineStyle=plain&_a=contents"

    @property
    def formatted_message(self):
        """Format the message with file location and URL."""
        # Use the trimmed rule_id without the TEST001- prefix
        rule_name = self.rule_id.split('-', 1)[-1] if '-' in self.rule_id else self.rule_id
        return f"{rule_name} at {self.file_path}:{self.line} | {self.file_url}"

    @property
    def azure_devops_message(self):
        """Format message for Azure DevOps logging."""
        return f"##vso[task.logissue type={self.severity}]{self.formatted_message}"

    @property
    def exclude(self):
        """
        Exclude certain findings:
        - Missing HTTP Headers
        - Findings without a valid file path (root path or empty)
        - Findings without a valid line number
        """
        if "Missing HTTP Header" in self.message:
            return True
        # Exclude findings that don't have a file path or are at root
        if self.file_path == "/" or self.file_path == "":
            return True
        # Exclude findings that don't have a line number
        if self.line == 0 or self.line is None or self.line == 1:
            return True
        return False

    def __str__(self):
        return self.formatted_message
