"""Settings and styles for PDF report generation."""
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet


class HeaderSettings:
    """Settings for header elements."""
    class Height:
        """Height settings for different header levels."""
        h1 = 20  # Main sections: "Findings"
        h2 = 16  # Major subsections: "Summary", "Finding Details"
        h3 = 14  # Severity groups: "Critical Severity Findings"
        h4 = 12  # Finding types: "SQL Injection"
        h5 = 11  # Instances: "Instance 1: SQL Injection"
    
    class Spacing:
        """Spacing settings for headers."""
        before_h1 = 12
        after_h1 = 0
        before_h2 = 12
        after_h2 = 0
        before_h3 = 12
        after_h3 = 0
        before_h4 = 8
        after_h4 = 4
        before_h5 = 6
        after_h5 = 12

    class Elements:
        """Mapping of document elements to header levels."""
        main_section = 'h1'      # "Findings"
        subsection = 'h2'        # "Summary", "Finding Details"
        severity_group = 'h3'    # "Critical Severity Findings"
        finding_type = 'h4'      # "SQL Injection"
        finding_instance = 'h5'  # "Instance 1: SQL Injection"


class PageSettings:
    """Page layout settings."""
    margin_top = 36
    margin_bottom = 72
    margin_left = 72
    margin_right = 72
    
    # Table settings
    table_left_indent = 20  # Indent for table alignment
    findings_table_widths = [4.5*inch, 1.25*inch, 0.75*inch]  # Finding Type, Severity, Count


class LogoSettings:
    """Logo settings."""
    width = 1.5 * inch
    height = 0.375 * inch


class SpacingSettings:
    """Spacing settings for various elements."""
    after_title = 12  # Spacing after the report title
    after_header = HeaderSettings.Spacing.after_h1
    after_subheader = HeaderSettings.Spacing.after_h2
    after_normal = 2
    after_section = 10
    after_finding = 6
    before_finding = 8
    after_instance = 4   # Space after each instance block
    before_instance = 0  # Space before each instance block


class ColorSettings:
    """Color settings for various elements."""
    class Severity:
        """Colors for different severity levels."""
        critical = '#960505'  # darkred
        high = '#FF0000'  # red
        medium = '#FF8C00'  # darkorange
        low = '#008000'  # green
        info = '#0000FF'  # blue
        unknown = colors.gray

    class Text:
        """Colors for different text elements."""
        title = colors.black
        header = '#050D54'
        link = '#0000EE'
        finding_title = colors.white

    class Background:
        """Background colors for different elements."""
        finding_title = '#0d6efd'
        table_alternate = '#f8f9fa'


class FontSettings:
    """Font settings for different text elements."""
    class Size:
        """Font sizes for different elements."""
        title = HeaderSettings.Height.h1
        header = HeaderSettings.Height.h1
        subheader = HeaderSettings.Height.h2
        finding_title = HeaderSettings.Height.h4
        instance_title = HeaderSettings.Height.h5
        normal = 10
        
    class Leading:
        """Line spacing for different elements."""
        normal = 14
        finding_title = 20
        instance_title = 16

    class Family:
        """Font families for different elements."""
        normal = 'Helvetica'
        bold = 'Helvetica-Bold'


class StyleFactory:
    """Creates and manages PDF styles."""
    
    @staticmethod
    def create_styles():
        """Create all styles used in the PDF report."""
        styles = getSampleStyleSheet()
        
        # Title style (Report Title)
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=FontSettings.Size.title,
            spaceAfter=SpacingSettings.after_title,
            alignment=TA_LEFT,
            textColor=ColorSettings.Text.title,
            fontName=FontSettings.Family.bold
        ))

        # H1 style (Main sections)
        styles.add(ParagraphStyle(
            name='Header',
            parent=styles['Heading1'],
            fontSize=HeaderSettings.Height.h1,
            spaceBefore=HeaderSettings.Spacing.before_h1,
            spaceAfter=HeaderSettings.Spacing.after_h1,
            textColor=colors.HexColor(ColorSettings.Text.header),
            fontName=FontSettings.Family.bold
        ))

        # H2 style (Major subsections)
        styles.add(ParagraphStyle(
            name='Subheader',
            parent=styles['Heading2'],
            fontSize=HeaderSettings.Height.h2,
            spaceBefore=HeaderSettings.Spacing.before_h2,
            spaceAfter=HeaderSettings.Spacing.after_h2,
            textColor=colors.HexColor(ColorSettings.Text.header),
            fontName=FontSettings.Family.bold
        ))

        # H3 style (Severity groups)
        styles.add(ParagraphStyle(
            name='SeverityHeader',
            parent=styles['Heading3'],
            fontSize=HeaderSettings.Height.h3,
            spaceBefore=HeaderSettings.Spacing.before_h3,
            spaceAfter=HeaderSettings.Spacing.after_h3,
            textColor=colors.HexColor(ColorSettings.Text.header),
            fontName=FontSettings.Family.bold
        ))

        # H4 style (Finding types)
        styles.add(ParagraphStyle(
            name='FindingTitle',
            parent=styles['Heading4'],
            fontSize=HeaderSettings.Height.h4,
            spaceBefore=HeaderSettings.Spacing.before_h4,
            spaceAfter=HeaderSettings.Spacing.after_h4,
            textColor=colors.HexColor(ColorSettings.Text.header),
            fontName=FontSettings.Family.bold,
            leading=FontSettings.Leading.finding_title
        ))

        # H5 style (Finding instances)
        styles.add(ParagraphStyle(
            name='InstanceTitle',
            parent=styles['Heading5'],
            fontSize=HeaderSettings.Height.h5,
            spaceBefore=HeaderSettings.Spacing.before_h5,
            spaceAfter=HeaderSettings.Spacing.after_h5,
            textColor=colors.HexColor(ColorSettings.Text.header),
            fontName=FontSettings.Family.bold,
            leading=FontSettings.Leading.instance_title
        ))

        # Normal text style
        styles.add(ParagraphStyle(
            name='NormalText',
            parent=styles['Normal'],
            fontSize=FontSettings.Size.normal,
            spaceAfter=SpacingSettings.after_normal,
            leading=FontSettings.Leading.normal,
            fontName=FontSettings.Family.normal
        ))

        # Right-aligned text for website
        styles.add(ParagraphStyle(
            name='RightAligned',
            parent=styles['Normal'],
            alignment=TA_RIGHT,
            fontSize=FontSettings.Size.normal,
            textColor=colors.HexColor(ColorSettings.Text.link),
            fontName=FontSettings.Family.normal
        ))

        # Link style
        styles.add(ParagraphStyle(
            name='Link',
            parent=styles['Normal'],
            textColor=colors.HexColor(ColorSettings.Text.link),
            fontSize=FontSettings.Size.normal,
            fontName=FontSettings.Family.normal
        ))

        return styles


class TableSettings:
    """Settings for tables in the PDF."""
    
    @staticmethod
    def get_findings_table_style():
        """Get the style for the findings table."""
        return [
            ('LEFTPADDING', (0, 0), (-1, -1), 6),  # Standard cell padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),  # Standard cell padding
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (-1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(ColorSettings.Background.table_alternate)])
        ]


class SeverityOrder:
    """Order of severity levels for sorting."""
    order = {
        'CRITICAL': 0,
        'HIGH': 1,
        'MEDIUM': 2,
        'LOW': 3,
        'INFORMATIONAL': 4,
        'UNKNOWN': 5
    }

    @staticmethod
    def format_severity(severity: str) -> str:
        """Format severity text for display."""
        return severity.title()  # Converts "CRITICAL" to "Critical"


class SeverityText:
    """Text representations of severity levels."""
    Critical = "Critical"
    High = "High"
    Medium = "Medium"
    Low = "Low"
    Informational = "Informational"
    Unknown = "Unknown"

    @staticmethod
    def get_display_text(severity: str) -> str:
        """Get the display text for a severity level."""
        mapping = {
            'CRITICAL': SeverityText.Critical,
            'HIGH': SeverityText.High,
            'MEDIUM': SeverityText.Medium,
            'LOW': SeverityText.Low,
            'INFORMATIONAL': SeverityText.Informational,
            'UNKNOWN': SeverityText.Unknown
        }
        return mapping.get(severity.upper(), SeverityText.Unknown)


class LetterheadSettings:
    """Settings for letterhead layout."""
    column_widths = [3.25*inch, 3.25*inch]
    website_url = 'nightvision.net'
    
    class Style:
        """Style settings for letterhead."""
        align_left = ('ALIGN', (0, 0), (0, 0), 'LEFT')
        align_right = ('ALIGN', (1, 0), (1, 0), 'RIGHT')
        valign_middle = ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        no_padding_top = ('TOPPADDING', (0, 0), (-1, -1), 0)
        no_padding_bottom = ('BOTTOMPADDING', (0, 0), (-1, -1), 0) 

