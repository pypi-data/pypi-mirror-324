"""PDF command for generating PDF reports from SARIF files."""
import click
import os
from sarif_manager.sarif.pdf_sarif import PDFSarif


@click.group("pdf")
def pdf():
    """Generate PDF reports from SARIF files."""


@pdf.command("generate", help="Generate a PDF report from a SARIF file.")
@click.argument('sarif_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--target-name', help="Name of the target system/application")
@click.option('--target-url', help="URL of the target system/application")
def generate_pdf(sarif_file, output_file, target_name, target_url):
    """Generate a PDF report from a SARIF file.
    
    Example:
        sarif-manager pdf generate example.sarif example.pdf --target-name "Example App" --target-url "https://example.com"
    
    Args:
        sarif_file: Path to the SARIF file
        output_file: Path where to save the PDF report
        target_name: Name of the target system/application
        target_url: URL of the target system/application
    """
    # Remove output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Generate PDF
    pdf_generator = PDFSarif()
    pdf_generator.load_from_file(sarif_file)
    
    # Set scan info
    scan_info = {
        'target': {
            'name': target_name,
            'url': target_url
        },
        'scan_id': None  # This will be extracted from the SARIF data
    }
    pdf_generator.set_scan_info(scan_info)
    
    if pdf_generator.generate_pdf(output_file):
        click.echo(f"Successfully generated PDF report at {output_file}")
    else:
        click.echo("Failed to generate PDF report", err=True)
        exit(1) 