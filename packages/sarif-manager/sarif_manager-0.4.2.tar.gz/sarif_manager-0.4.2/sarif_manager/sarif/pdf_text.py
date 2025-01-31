"""Text formatting utilities for PDF report generation."""
from datetime import datetime


class PDFTextFormatter:
    """Formats text for PDF report elements."""

    @staticmethod
    def format_target_info(name: str) -> str:
        """Format target name."""
        return f"<b>Target:</b> {name}"

    @staticmethod
    def format_target_url(url: str) -> str:
        """Format target URL."""
        return f"<b>URL:</b> {url}"

    @staticmethod
    def format_scan_url(scan_id: str) -> str:
        """Format scan URL with hyperlink."""
        url = f"https://app.nightvision.net/scans/{scan_id}"
        return f"<b>Scan:</b> <link color='blue' href='{url}'><u>{url}</u></link>"

    @staticmethod
    def format_timestamp(timestamp: datetime) -> str:
        """Format timestamp."""
        return f"<b>Report Generated:</b> {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}"

    @staticmethod
    def format_finding_link(title: str) -> str:
        """Format finding title as a link."""
        anchor_id = title.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
        return f'<link color="blue" href="#{anchor_id}">{title}</link>'

    @staticmethod
    def format_finding_anchor(title: str) -> str:
        """Format finding title with anchor."""
        anchor_id = title.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
        return f'<a name="{anchor_id}"/>{title}'

    @staticmethod
    def format_instance_number(number: int) -> str:
        """Format instance number."""
        return f"Instance {number}:"

    @staticmethod
    def format_location(location: str) -> str:
        """Format finding location."""
        return f"Location: {location}"

    @staticmethod
    def format_finding_link_info(url: str) -> str:
        """Format finding link information."""
        return f'For more information see the issue on NightVision here: <link color="blue" href="{url}">{url}</link>'

    @staticmethod
    def format_severity_count(severity: str, count: int) -> str:
        """Format severity count bullet point."""
        return f"• {severity}: {count}" 