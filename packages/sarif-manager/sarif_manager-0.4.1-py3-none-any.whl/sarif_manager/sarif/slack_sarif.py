from typing import Union
import json
import ssl
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackSarif:
    # Base URL for NightVision
    NIGHTVISION_BASE_URL = "https://app.nightvision.net"

    def __init__(self):
        self.sarif_data = {}
        self.sarif_findings = []
        self.slack_token: Union[str, None] = None
        self.slack_channel: Union[str, None] = None
        self.slack_client: Union[WebClient, None] = None
        self.scan_id: Union[str, None] = None

    def load_from_file(self, sarif_file: str):
        """Load SARIF data from a file."""
        with open(sarif_file, 'r') as file:
            self.sarif_data = json.load(file)
        self.parse()

    def set_auth(self, token: str):
        """Set Slack authentication token and initialize client."""
        self.slack_token = token
        # Create a custom SSL context that doesn't verify certificates
        # If we don't do this, we get a strange certificate error from slack depending on the machine that we are sending it from.
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        self.slack_client = WebClient(
            token=token,
            ssl=ssl_context
        )

    def set_channel(self, channel: str):
        """Set Slack channel for messages."""
        self.slack_channel = channel

    def _extract_scan_id_from_uri(self, uri: str) -> str:
        """Extract scan ID from a NightVision URI.
        
        Args:
            uri (str): The URI containing the scan ID
            
        Returns:
            str: The extracted scan ID
        """
        if 'scans/' in uri:
            parts = uri.split('/')
            for i, part in enumerate(parts):
                if part == 'scans' and i + 1 < len(parts):
                    return parts[i + 1]
        return None

    def _extract_issue_type_id_from_help(self, help_text: str) -> str:
        """Extract issue type ID from help text by finding the findings URL.
        
        Args:
            help_text (str): The help text containing the findings URL
            
        Returns:
            str: The issue type ID extracted from the URL
        """
        if not help_text:
            return None
            
        # Look for URL pattern in help text
        import re
        pattern = r'https://app\.nightvision\.net/scans/[^/]+/findings/(\d+)'
        match = re.search(pattern, help_text)
        if match:
            return match.group(1)
        return None

    def _clean_rule_name(self, rule_id: str, issue_id: str) -> str:
        """Clean rule name by removing issue ID prefix.
        
        Args:
            rule_id (str): The full rule ID
            issue_id (str): The issue ID to strip from the rule ID
            
        Returns:
            str: The cleaned rule name
        """
        if issue_id and rule_id.startswith(issue_id):
            # Remove the issue ID and the following hyphen
            return rule_id[len(issue_id) + 1:].strip()
        return rule_id

    def _extract_issue_id(self, result: dict) -> str:
        """Extract issue ID from a finding result.
        
        Args:
            result (dict): The SARIF result object
            
        Returns:
            str: The issue ID from the fingerprints, or None if not found
        """
        return result.get('partialFingerprints', {}).get('nightvisionIssueID/v1')

    def _get_finding_severity(self, result: dict) -> str:
        """Get the severity level from nightvision-risk property.
        
        Args:
            result (dict): The SARIF result object
            
        Returns:
            str: The severity level (CRITICAL, HIGH, MEDIUM, LOW, or INFORMATIONAL)
        """
        return result.get('properties', {}).get('nightvision-risk', 'INFORMATIONAL')

    def _create_scan_link(self) -> str:
        """Create the full URL for the scan results.
        
        Returns:
            str: The complete URL to the scan results
        """
        if not self.scan_id:
            self.scan_id = self._extract_scan_id_from_uri(self.sarif_data.get('runs', [{}])[0].get('tool', {}).get('driver', {}).get('informationUri', ''))
        return f"{self.NIGHTVISION_BASE_URL}/scans/{self.scan_id}/findings"

    def _create_issue_link(self, scan_id: str, issue_type_id: str, rule_name: str) -> str:
        """Create a formatted Slack markdown link for an issue.
        
        Args:
            scan_id (str): The scan ID
            issue_type_id (str): The issue type ID
            rule_name (str): The name of the rule/finding
            
        Returns:
            str: Formatted Slack markdown link
        """
        if scan_id and issue_type_id:
            url = f"{self.NIGHTVISION_BASE_URL}/scans/{scan_id}/findings/{issue_type_id}"
            return f"<{url}|{rule_name}>"
        return rule_name

    def parse(self):
        """Parse SARIF data into findings."""
        # Extract scan ID from informationUri in tool driver
        for run in self.sarif_data.get('runs', []):
            tool_driver = run.get('tool', {}).get('driver', {})
            info_uri = tool_driver.get('informationUri', '')
            if info_uri:
                self.scan_id = self._extract_scan_id_from_uri(info_uri)
                break
        
        for run in self.sarif_data.get('runs', []):
            for result in run.get('results', []):
                # Get rule details
                rule_id = result.get('ruleId', '')
                rule_details = None
                for rule in run['tool']['driver']['rules']:
                    if rule['id'] == rule_id:
                        rule_details = rule
                        break

                # Get location details
                location = result.get('locations', [{}])[0].get('physicalLocation', {})
                file_uri = location.get('artifactLocation', {}).get('uri', '')
                line = location.get('region', {}).get('startLine', 0)

                # Extract issue type ID from help text
                issue_type_id = None
                if rule_details:
                    help_text = rule_details.get('help', {}).get('text', '')
                    issue_type_id = self._extract_issue_type_id_from_help(help_text)

                # Extract issue ID and clean rule name
                issue_id = self._extract_issue_id(result)
                rule_name = self._clean_rule_name(rule_id, issue_id)

                finding = {
                    'rule_id': rule_id,
                    'rule_name': rule_name,
                    'message': result.get('message', {}).get('text', ''),
                    'severity': self._get_finding_severity(result),
                    'location': file_uri,
                    'line': line,
                    'description': rule_details['fullDescription']['text'] if rule_details else 'No description available.',
                    'issue_id': issue_id,
                    'issue_type_id': issue_type_id
                }
                self.sarif_findings.append(finding)

    def _get_severity_emoji(self, severity: str) -> str:
        """Get emoji for severity level.
        
        Args:
            severity (str): The severity level
            
        Returns:
            str: The corresponding emoji
        """
        severity_map = {
            'CRITICAL': '❌',
            'HIGH': '⚠️',
            'MEDIUM': '🟠',
            'LOW': '🔵',
            'INFORMATIONAL': '⚪️'
        }
        return severity_map.get(severity, '⚪️')

    def _has_no_code_traceback(self, location: str, line: int) -> bool:
        """Check if the finding has no code traceback. Findings with no traceback will
        have a code path of / and line number of 1. We do not want to display these in the
        slack message.

        Args:
            location (str): The file location
            line (int): The line number

        Returns:
            bool: True if no code traceback, False otherwise
        """
        return location == "/" and line == 1

    def _group_findings_by_severity(self):
        """Group findings by severity level and deduplicate by rule name.
        
        Returns:
            dict: Findings grouped by severity level
        """
        severity_groups = {
            'CRITICAL': [],
            'HIGH': [],
            'MEDIUM': [],
            'LOW': [],
            'INFORMATIONAL': []
        }
        
        seen_rules = set()
        for finding in self.sarif_findings:
            severity = finding.get('severity', 'INFORMATIONAL')
            rule_name = finding.get('rule_name', '').strip()
            
            # Skip if we've seen this rule name before
            if rule_name in seen_rules:
                continue
                
            seen_rules.add(rule_name)
            severity_groups[severity].append(finding)
            
        return severity_groups

    def _format_finding_block(self, finding):
        """Create a Slack block for a finding.

        Args:
            finding (dict): The finding details

        Returns:
            dict: Slack block for the finding
        """
        link = self._create_issue_link(
            scan_id=self.scan_id,
            issue_type_id=finding['issue_type_id'],
            rule_name=finding['rule_name']
        )
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"• {link}. Code Location: `{finding['location']}:{finding['line']}`"
            }
        }


    def format_slack_message(self):
        """Format findings into a Slack message using Block Kit.
        
        Returns:
            list: List of Slack blocks for the message
        """
        severity_groups = self._group_findings_by_severity()
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🔒 NightVision Security Scan Results 🔒",
                    "emoji": True
                }
            },
            {"type": "divider"}
        ]

        # Add findings summary section
        summary_text = "*Findings Summary*\n"
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFORMATIONAL']:
            findings = severity_groups[severity]
            if findings:
                emoji = self._get_severity_emoji(severity)
                summary_text += f"{emoji} {severity.title()} Severity: {len(findings)}\n"

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": summary_text
            }
        })

        # Only add scan samples if there are Critical or High severity findings
        if severity_groups['CRITICAL'] or severity_groups['HIGH']:
            blocks.append({"type": "divider"})
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Scan Samples*"
                }
            })

            # Add Critical findings
            if severity_groups['CRITICAL']:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "_*Critical Severity*_:"
                    }
                })
                for finding in severity_groups['CRITICAL']:
                    if not self._has_no_code_traceback(location=finding["location"], line=finding["line"]):
                        blocks.append(self._format_finding_block(finding))

            # Add High severity findings
            if severity_groups['HIGH']:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "_*High Severity*_:"
                    }
                })
                for finding in severity_groups['HIGH']:
                    if not self._has_no_code_traceback(location=finding["location"], line=finding["line"]):
                        blocks.append(self._format_finding_block(finding))

        # Add references
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*References:*\n• <{self._create_scan_link()}|NightVision Scan Results>"
            }
        })

        return blocks

    def send_to_slack(self):
        """Send formatted findings to Slack.
        
        Returns:
            dict: Slack API response
            
        Raises:
            ValueError: If Slack client is not initialized or channel is not set
            SlackApiError: If there's an error sending the message to Slack
        """
        if not self.slack_client or not self.slack_channel:
            raise ValueError("Slack client not initialized or channel not set")

        blocks = self.format_slack_message()
        
        try:
            response = self.slack_client.chat_postMessage(
                channel=self.slack_channel,
                text="Security Scan Results",
                blocks=blocks
            )
            return response
        except SlackApiError as e:
            print(f"Error sending message to Slack: {e.response['error']}")
            raise
