from importlib.metadata import requires

import click
from click_option_group import optgroup
from sarif_manager.sarif.slack_sarif import SlackSarif
from sarif_manager.sarif.pdf_sarif import PDFSarif
import tempfile
import os


@click.group("slack")
def slack():
    """Manage Slack notifications."""


@slack.command("send", help="Send SARIF findings to a Slack channel.")
@click.argument("sarif-file", type=click.Path(exists=True))
@optgroup.group("Slack Details")
@optgroup.option("--channel", help="Slack channel ID", required=True, envvar="SLACK_CHANNEL")
@optgroup.option("--token", help="Slack bot token", required=True, envvar="SLACK_BOT_TOKEN")
@optgroup.option("--attach-pdf", is_flag=True, help="Attach a PDF report of the findings")
@optgroup.group("Target Details")
@optgroup.option('--target-name', help="Name of the target (Optional)", required=False)
@optgroup.option('--target-url', help="URL of the target (Optional)", required=False)
def send_to_slack(sarif_file, channel, token, attach_pdf, target_name, target_url):
    """Send SARIF findings to a Slack channel."""
    slack_sarif = SlackSarif()
    slack_sarif.set_auth(token)
    slack_sarif.set_channel(channel)
    slack_sarif.load_from_file(sarif_file)

    # Generate PDF if requested
    pdf_path = None
    if attach_pdf:
        pdf_generator = PDFSarif()
        pdf_generator.load_from_file(sarif_file)
        scan_info = {
            'target': {
                'name': target_name,
                'url': target_url
            },
            'scan_id': None  # This will be extracted from the SARIF data
        }
        pdf_generator.set_scan_info(scan_info)
        # Create temporary file for PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            pdf_path = tmp_file.name
        
        if not pdf_generator.generate_pdf(pdf_path):
            click.echo("Failed to generate PDF report", err=True)
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)
            return

    # Send to Slack
    response = slack_sarif.send_to_slack(pdf_file=pdf_path if attach_pdf else None)
    
    # Clean up PDF file
    if pdf_path and os.path.exists(pdf_path):
        os.unlink(pdf_path)

    if response and response["ok"]:
        click.echo("Successfully sent findings to Slack!")
    else:
        click.echo("Failed to send findings to Slack", err=True)

