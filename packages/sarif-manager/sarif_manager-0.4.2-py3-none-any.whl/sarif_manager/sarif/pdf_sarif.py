"""Module for generating PDF reports from SARIF findings."""
from datetime import datetime, timezone
import os
from dataclasses import dataclass
from typing import List, Dict, Optional
import markdown
from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image
)
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from loguru import logger
from .pdf_settings import (
    PageSettings, LogoSettings, SpacingSettings, ColorSettings,
    StyleFactory, TableSettings, SeverityOrder
)
from .pdf_text import PDFTextFormatter
from .pdf_findings import FindingsOverviewGenerator
from .pdf_letterhead import LetterheadGenerator
from .pdf_finding_details import FindingDetailsGenerator


@dataclass
class Finding:
    """Represents a single finding with all its details."""
    title: str
    severity: str
    location: Optional[str]
    description: Optional[str]
    scan_url: Optional[str]


@dataclass
class Target:
    """Represents the target of the scan."""
    name: Optional[str]
    url: Optional[str]


@dataclass
class ScanInfo:
    """Contains all information about the scan."""
    target: Target
    scan_id: Optional[str]
    timestamp: datetime


class FindingsProcessor:
    """Processes raw findings data into structured format."""
    
    @staticmethod
    def should_include_finding(finding: Finding) -> bool:
        """Determine if a finding should be included in the report."""
        return "Missing HTTP Header" not in finding.title

    @staticmethod
    def convert_raw_to_finding(raw_finding: Dict) -> Finding:
        """Convert a raw finding dictionary to a Finding object."""
        return Finding(
            title=raw_finding.get('title', 'Untitled Finding'),
            severity=raw_finding.get('severity', 'UNKNOWN'),
            location=raw_finding.get('location'),
            description=raw_finding.get('description'),
            scan_url=raw_finding.get('scan_url')
        )

    @classmethod
    def process_findings(cls, raw_findings: List[Dict]) -> Dict:
        """Process raw findings into structured data for the report."""
        findings = [cls.convert_raw_to_finding(f) for f in raw_findings]
        included_findings = [f for f in findings if cls.should_include_finding(f)]
        
        # Group findings by severity and type
        findings_by_severity = {}
        severity_counts = {}
        
        for finding in included_findings:
            # Count by severity
            if finding.severity not in severity_counts:
                severity_counts[finding.severity] = 0
            severity_counts[finding.severity] += 1
            
            # Group by severity and title
            if finding.severity not in findings_by_severity:
                findings_by_severity[finding.severity] = {}
            if finding.title not in findings_by_severity[finding.severity]:
                findings_by_severity[finding.severity][finding.title] = []
            findings_by_severity[finding.severity][finding.title].append(finding)
        
        return {
            'findings_by_severity': findings_by_severity,
            'severity_counts': severity_counts
        }


class PDFSarif:
    """Class to generate PDF reports from SARIF findings."""

    def __init__(self):
        """Initialize PDFSarif."""
        self.findings_data = None
        self.scan_info = None
        self.styles = StyleFactory.create_styles()
        self.letterhead_generator = LetterheadGenerator(self.styles)
        self.findings_generator = FindingsOverviewGenerator(self.styles)
        self.details_generator = FindingDetailsGenerator(self.styles)
        self.sarif_data = None

    def _extract_scan_id_from_uri(self, uri: str) -> str:
        """Extract scan ID from a NightVision URI."""
        if 'scans/' in uri:
            parts = uri.split('/')
            for i, part in enumerate(parts):
                if part == 'scans' and i + 1 < len(parts):
                    return parts[i + 1]
        return None

    def _extract_issue_type_id_from_help(self, help_text: str) -> str:
        """Extract issue type ID from help text by finding the findings URL."""
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
        """Clean rule name by removing issue ID prefix."""
        # First try to split on the first hyphen after the UUID
        import re
        match = re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}-(.+)$', rule_id)
        if match:
            return match.group(1).strip()
        
        # Fallback to old method
        if issue_id and rule_id.startswith(issue_id):
            return rule_id[len(issue_id) + 1:].strip()
        
        return rule_id

    def _extract_issue_id(self, result: dict) -> str:
        """Extract issue ID from a finding result."""
        return result.get('partialFingerprints', {}).get('nightvisionIssueID/v1')

    def _get_finding_severity(self, result: dict) -> str:
        """Get the severity level from nightvision-risk property."""
        return result.get('properties', {}).get('nightvision-risk', 'INFORMATIONAL')

    def load_from_file(self, sarif_file: str):
        """Load SARIF data from a file."""
        import json
        with open(sarif_file, 'r') as file:
            self.sarif_data = json.load(file)
        self._process_sarif_data()

    def _process_sarif_data(self):
        """Process SARIF data into findings."""
        findings = []
        for run in self.sarif_data.get('runs', []):
            # Get rules lookup
            rules = {}
            for rule in run['tool']['driver'].get('rules', []):
                rules[rule['id']] = rule
            
            # Process each result
            for result in run.get('results', []):
                rule_id = result.get('ruleId', '')
                rule = rules.get(rule_id, {})
                
                # Get location details
                location = result.get('locations', [{}])[0].get('physicalLocation', {})
                file_uri = location.get('artifactLocation', {}).get('uri', '')
                line = location.get('region', {}).get('startLine', 0)
                
                # Extract issue type ID from help text
                issue_type_id = None
                if rule:
                    help_text = rule.get('help', {}).get('text', '')
                    issue_type_id = self._extract_issue_type_id_from_help(help_text)
                
                # Extract issue ID and clean rule name
                issue_id = self._extract_issue_id(result)
                rule_name = self._clean_rule_name(rule_id, issue_id)
                
                finding = {
                    'title': rule_name,
                    'severity': self._get_finding_severity(result),
                    'location': file_uri,
                    'line': line,
                    'description': rule.get('fullDescription', {}).get('text', ''),
                    'issue_id': issue_id,
                    'issue_type_id': issue_type_id
                }
                findings.append(finding)
        
        # Extract scan ID
        scan_id = None
        for run in self.sarif_data.get('runs', []):
            tool_driver = run.get('tool', {}).get('driver', {})
            info_uri = tool_driver.get('informationUri', '')
            if info_uri:
                scan_id = self._extract_scan_id_from_uri(info_uri)
                if scan_id:
                    break
        
        # Update findings with scan URLs if scan_id is provided
        if scan_id:
            base_url = "https://app.nightvision.net/scans"
            for finding in findings:
                if issue_id := finding.get('issue_type_id'):
                    finding['scan_url'] = f"{base_url}/{scan_id}/findings/{issue_id}"
        
        # Process findings into the format needed for the PDF
        self.findings_data = FindingsProcessor.process_findings(findings)

    def _markdown_to_html(self, text):
        """Convert markdown text to HTML."""
        html = markdown.markdown(text)
        soup = BeautifulSoup(html, 'html.parser')
        return str(soup)

    def _create_header(self):
        """Create the report header section."""
        elements = []
        
        # Add letterhead
        if letterhead := self.letterhead_generator.generate():
            elements.append(letterhead)
        
        # Title
        elements.append(Paragraph("NightVision Vulnerability Scan Report", self.styles['CustomTitle']))
        
        # Target info section
        if self.scan_info:
            if self.scan_info.target.name:
                elements.append(Paragraph(
                    PDFTextFormatter.format_target_info(self.scan_info.target.name),
                    self.styles['NormalText']
                ))
            if self.scan_info.target.url:
                elements.append(Paragraph(
                    PDFTextFormatter.format_target_url(self.scan_info.target.url),
                    self.styles['NormalText']
                ))
            if self.scan_info.scan_id:
                elements.append(Paragraph(
                    PDFTextFormatter.format_scan_url(self.scan_info.scan_id),
                    self.styles['NormalText']
                ))
            
            # Add timestamp
            elements.append(Paragraph(
                PDFTextFormatter.format_timestamp(self.scan_info.timestamp),
                self.styles['NormalText']
            ))
        
        elements.append(Spacer(1, SpacingSettings.after_section))
        return elements

    def _create_findings_overview(self):
        """Create the findings overview section."""
        return self.findings_generator.generate(self.findings_data)

    def _format_finding_details(self):
        """Format all findings details, grouped by severity and type."""
        return self.details_generator.generate(self.findings_data)

    def set_scan_info(self, raw_scan_info: Dict):
        """Set scan information."""
        self.scan_info = ScanInfo(
            target=Target(
                name=raw_scan_info.get('target', {}).get('name'),
                url=raw_scan_info.get('target', {}).get('url')
            ),
            scan_id=raw_scan_info.get('scan_id'),
            timestamp=datetime.now(timezone.utc)
        )

    def add_findings(self, raw_findings: List[Dict]):
        """Process and add findings data."""
        self.findings_data = FindingsProcessor.process_findings(raw_findings)

    def generate_pdf(self, output_path: str) -> bool:
        """Generate PDF report with the findings."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=PageSettings.margin_right,
            leftMargin=PageSettings.margin_left,
            topMargin=PageSettings.margin_top,
            bottomMargin=PageSettings.margin_bottom
        )

        elements = []
        elements.extend(self._create_header())
        elements.extend(self._create_findings_overview())
        elements.extend(self._format_finding_details())

        try:
            doc.build(elements)
            logger.info(f"PDF report generated successfully at {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate PDF report: {str(e)}")
            return False 
