"""Finding details generation for PDF reports."""
from typing import List, Dict
from reportlab.platypus import Paragraph, Spacer
import markdown
from xhtml2pdf.parser import pisaParser
from xhtml2pdf.context import pisaContext
from xhtml2pdf.document import pisaDocument
from io import BytesIO
from .pdf_settings import SpacingSettings, SeverityOrder, SeverityText
from .pdf_text import PDFTextFormatter


class FindingDetailsGenerator:
    """Generates the finding details section of the PDF report."""

    def __init__(self, styles):
        """Initialize with styles dictionary."""
        self.styles = styles
        # Configure GitHub-flavored markdown extensions
        self.markdown_extensions = [
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists'
        ]

    def _markdown_to_html(self, text: str) -> str:
        """Convert GitHub-flavored markdown to HTML with basic styling."""
        html = markdown.markdown(text, extensions=self.markdown_extensions)
        # Add basic CSS for code blocks and other elements
        styled_html = f"""
        <div style="font-family: Helvetica; font-size: 10pt;">
            <style>
                code {{ font-family: Courier; background-color: #f6f8fa; padding: 2px 4px; }}
                pre {{ background-color: #f6f8fa; padding: 8px; margin: 4px 0; }}
                ul {{ margin: 4px 0; padding-left: 20px; }}
                p {{ margin: 4px 0; }}
            </style>
            {html}
        </div>
        """
        return styled_html

    def _create_section_header(self) -> List:
        """Create the section header."""
        elements = []
        elements.append(Paragraph("Finding Details", self.styles['Header']))
        elements.append(Spacer(1, SpacingSettings.after_finding))
        return elements

    def _create_severity_header(self, severity: str) -> List:
        """Create a severity section header."""
        elements = []
        display_text = SeverityText.get_display_text(severity)
        elements.append(Paragraph(
            f"{display_text} Severity Findings",
            self.styles['SeverityHeader']
        ))
        return elements

    def _create_finding_title(self, title: str) -> List:
        """Create a finding title with anchor."""
        elements = []
        elements.append(Paragraph(
            PDFTextFormatter.format_finding_anchor(title),
            self.styles['FindingTitle']
        ))
        return elements

    def _clean_description(self, text: str) -> str:
        """Clean up the description text before markdown conversion."""
        # Remove emojis but keep the text
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove emojis and clean up extra spaces
            cleaned_line = line
            for emoji in ['🚨', 'ℹ️', '🔍', '⬛']:
                cleaned_line = cleaned_line.replace(emoji, '')
            # Remove "Exploitable Vulnerability Found" header
            if 'Exploitable Vulnerability Found' in cleaned_line:
                continue
            # Clean up extra spaces and only add non-empty lines
            cleaned_line = ' '.join(cleaned_line.split())
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
        return '\n'.join(cleaned_lines)

    def _create_instance_details(self, finding, instance_num: int) -> List:
        """Create the details for a single finding instance."""
        elements = []
        
        # Instance title with location
        if finding.location:
            instance_text = f"Instance {instance_num}: {finding.location}"
            elements.append(Paragraph(instance_text, self.styles['InstanceTitle']))
        else:
            instance_text = f"Instance {instance_num}"
            elements.append(Paragraph(instance_text, self.styles['InstanceTitle']))
        
        # Add space after instance title
        elements.append(Spacer(1, SpacingSettings.after_normal * 4))
        
        # Description handling
        if finding.description:
            # Clean up the description
            clean_desc = self._clean_description(finding.description)
            
            # Split into lines first
            lines = clean_desc.split('\n')
            
            for i, line in enumerate(lines):
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Handle description header
                if '**Description**:' in line:
                    # Split the description header from the rest
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        # Add the header
                        elements.append(Paragraph('<b>Description:</b>', self.styles['NormalText']))
                        elements.append(Spacer(1, SpacingSettings.after_normal * 4))
                        # Add the content as a separate paragraph
                        content = parts[1].strip()
                        if content:
                            # Convert markdown for this line
                            html = markdown.markdown(content, extensions=self.markdown_extensions)
                            html = html.replace('<code>', '<font face="Courier" size="9" color="#FF1493">')
                            html = html.replace('</code>', '</font>')
                            elements.append(Paragraph(html, self.styles['NormalText']))
                            elements.append(Spacer(1, SpacingSettings.after_normal * 4))
                    else:
                        elements.append(Paragraph('<b>Description:</b>', self.styles['NormalText']))
                        elements.append(Spacer(1, SpacingSettings.after_normal * 4))
                
                # Handle "For more information" section
                elif line.startswith('For more information'):
                    # If it starts with "For more information", get the link and save it as a variable
                    link = line.split('https://')[1].strip()
                    link = f'https://{link}'
                    # Format with markdown-style link
                    elements.append(Paragraph(
                        PDFTextFormatter.format_finding_link_info(link),
                        self.styles['NormalText']
                    ))
                
                # Regular line
                else:
                    # Check for section headers
                    if line.strip() in ['## Summary', '## Solution']:
                        # Convert markdown for this line and make it bold
                        header = line.strip().replace('## ', '')
                        elements.append(Paragraph(f'<b>{header}:</b>', self.styles['NormalText']))
                        elements.append(Spacer(1, SpacingSettings.after_normal * 4))
                    else:
                        # Convert markdown for this line
                        html = markdown.markdown(line.strip(), extensions=self.markdown_extensions)
                        # Convert code blocks to use monospace font with pink color
                        html = html.replace('<code>', '<font face="Courier" size="9" color="#FF1493">')
                        html = html.replace('</code>', '</font>')
                        elements.append(Paragraph(html, self.styles['NormalText']))
                        elements.append(Spacer(1, SpacingSettings.after_normal * 4))
        
        return elements

    def _format_inline_code(self, text: str) -> str:
        """Format inline code segments with monospace font."""
        # Look for text between single quotes and format as code
        parts = text.split("'")
        for i in range(1, len(parts), 2):
            if i < len(parts):
                parts[i] = f'<font face="Courier" size="9">{parts[i]}</font>'
        return "'".join(parts)

    def _process_findings_by_severity(self, findings_by_severity: Dict) -> List:
        """Process all findings grouped by severity."""
        elements = []
        
        # Get sorted severities
        severities = sorted(
            findings_by_severity.keys(),
            key=lambda x: SeverityOrder.order.get(x, 99)
        )
        
        # Process each severity level
        for severity in severities:
            elements.extend(self._create_severity_header(severity))
            findings = findings_by_severity[severity]
            
            # Process each finding type
            for title, instances in findings.items():
                elements.extend(self._create_finding_title(title))
                
                # Process each instance
                for i, finding in enumerate(instances, 1):
                    elements.extend(self._create_instance_details(finding, i))
        
        return elements

    def generate(self, findings_data: Dict) -> List:
        """Generate the complete finding details section."""
        elements = []
        
        # Add section header
        elements.extend(self._create_section_header())
        
        # Process all findings
        elements.extend(self._process_findings_by_severity(
            findings_data['findings_by_severity']
        ))
        
        return elements 

