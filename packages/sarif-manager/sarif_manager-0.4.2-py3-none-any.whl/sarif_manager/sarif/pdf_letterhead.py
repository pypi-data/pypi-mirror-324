"""Letterhead generation for PDF reports."""
import os
from typing import List
from reportlab.platypus import Table, TableStyle, Paragraph, Image
from .pdf_settings import LogoSettings, LetterheadSettings


class LetterheadGenerator:
    """Generates the letterhead for PDF reports."""

    def __init__(self, styles):
        """Initialize with styles dictionary."""
        self.styles = styles

    def _get_logo(self) -> Image:
        """Get the logo image."""
        logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"Logo file not found at {logo_path}")
        return Image(logo_path, width=LogoSettings.width, height=LogoSettings.height)

    def _get_website(self) -> Paragraph:
        """Get the website text."""
        return Paragraph(LetterheadSettings.website_url, self.styles['RightAligned'])

    def _create_table_style(self) -> TableStyle:
        """Create the table style for letterhead."""
        return TableStyle([
            LetterheadSettings.Style.align_left,
            LetterheadSettings.Style.align_right,
            LetterheadSettings.Style.valign_middle,
            LetterheadSettings.Style.no_padding_top,
            LetterheadSettings.Style.no_padding_bottom,
        ])

    def generate(self) -> Table:
        """Generate the letterhead table."""
        try:
            logo = self._get_logo()
            website = self._get_website()
            
            letterhead = Table(
                [[logo, website]], 
                colWidths=LetterheadSettings.column_widths
            )
            letterhead.setStyle(self._create_table_style())
            return letterhead
            
        except FileNotFoundError as e:
            # If logo is missing, return None so calling code can handle it
            return None 