"""Findings overview generation for PDF reports."""
from typing import List, Dict
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
import markdown
from bs4 import BeautifulSoup
from .pdf_settings import (
    SpacingSettings, ColorSettings, PageSettings,
    TableSettings, SeverityOrder, SeverityText
)
from .pdf_text import PDFTextFormatter


class FindingsOverviewGenerator:
    """Generates the findings overview section of the PDF report."""

    def __init__(self, styles: Dict[str, ParagraphStyle]):
        """Initialize with styles dictionary."""
        self.styles = styles
        # Configure GitHub-flavored markdown extensions
        self.markdown_extensions = [
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists'
        ]

    def _convert_markdown_to_html(self, text: str) -> str:
        """Convert GitHub-flavored markdown to HTML."""
        # Convert markdown to HTML with GitHub-flavored markdown extensions
        html = markdown.markdown(text, extensions=self.markdown_extensions)
        
        # Use BeautifulSoup to clean and format the HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Convert code blocks to use monospace font
        for code in soup.find_all(['code', 'pre']):
            code['face'] = 'Courier'
            
        # Ensure lists are properly formatted
        for ul in soup.find_all('ul'):
            for li in ul.find_all('li'):
                li.string = '• ' + li.get_text()
        
        return str(soup)

    def create_severity_counts(self, severity_counts: Dict[str, int]) -> List:
        """Create severity count bullet points."""
        elements = []
        severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        
        for severity in severities:
            if count := severity_counts.get(severity, 0):
                display_text = SeverityText.get_display_text(severity)
                text = PDFTextFormatter.format_severity_count(display_text, count)
                elements.append(Paragraph(text, self.styles['NormalText']))
        
        return elements

    def _create_severity_cell(self, severity: str) -> Paragraph:
        """Create a styled severity cell."""
        display_text = SeverityText.get_display_text(severity)
        style = ParagraphStyle(
            f'Cell_{severity}',
            parent=self.styles['NormalText'],
            textColor=colors.HexColor(
                getattr(ColorSettings.Severity, severity.lower(), ColorSettings.Severity.unknown)
            ),
            fontName='Helvetica-Bold'
        )
        return Paragraph(display_text, style)

    def _create_description_cell(self, text: str) -> Paragraph:
        """Create a cell with markdown-formatted description."""
        if not text:
            return None
        html = self._convert_markdown_to_html(text)
        return Paragraph(html, self.styles['NormalText'])

    def _create_findings_table(self, findings_data: Dict) -> Table:
        """Create the findings table."""
        # Table headers
        data = [['Finding Type', 'Severity', 'Count']]
        
        # Sort severities
        severities = sorted(
            findings_data['findings_by_severity'].keys(),
            key=lambda x: SeverityOrder.order.get(x, 99)
        )
        
        # Build table rows
        for severity in severities:
            findings = findings_data['findings_by_severity'][severity]
            for title, instances in findings.items():
                # Create the title cell with link
                title_cell = Paragraph(PDFTextFormatter.format_finding_link(title), self.styles['Link'])
                
                # Create the severity cell
                severity_cell = self._create_severity_cell(severity)
                
                # Create the count cell
                count_cell = Paragraph(str(len(instances)), self.styles['NormalText'])
                
                data.append([title_cell, severity_cell, count_cell])
        
        # Create table with indent
        table = Table(
            data,
            colWidths=PageSettings.findings_table_widths,
            style=TableSettings.get_findings_table_style(),
            hAlign='LEFT'
        )
        return table

    def generate(self, findings_data: Dict) -> List:
        """Generate the complete findings overview section."""
        elements = []
        
        # Add headers
        elements.append(Paragraph("Findings", self.styles['Header']))
        elements.append(Spacer(1, SpacingSettings.after_finding))
        elements.append(Paragraph("Summary", self.styles['Subheader']))
        elements.append(Spacer(1, SpacingSettings.after_finding))
        
        # Add severity counts
        elements.extend(self.create_severity_counts(findings_data['severity_counts']))
        elements.append(Spacer(1, SpacingSettings.after_section))
        
        # Add findings table
        table = self._create_findings_table(findings_data)
        elements.append(table)
        elements.append(Spacer(1, SpacingSettings.after_section))
        
        return elements 

