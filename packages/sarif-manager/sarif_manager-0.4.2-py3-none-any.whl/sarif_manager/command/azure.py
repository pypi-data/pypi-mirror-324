import click
from click_option_group import optgroup
from sarif_manager.sarif.azure_sarif import AzureSarif


@click.group("azure")
def azure():
    """Manage Azure DevOps artifacts."""


@azure.command("write-logs", help="Write discovered findings to logs in Azure Pipelines.")
@click.argument("sarif-file", type=click.Path(exists=True))
@optgroup.group("Repository Details")
@optgroup.option("--org", "organization", help="Repository URL")
@optgroup.option("--project", help="Azure DevOps project name")
def write_logs(sarif_file, organization, project):
    """Write discovered findings to logs in Azure Pipelines."""
    azure_sarif = AzureSarif()
    azure_sarif.set_metadata(organization, project)
    azure_sarif.load_from_file(sarif_file)
    azure_sarif.print_logging_commands()


@azure.command("create-work-items", help="Create work items in Azure DevOps for each finding.")
@click.argument("sarif-file", type=click.Path(exists=True))
@click.option("--write-logs", is_flag=True, help="Write discovered findings to logs in Azure Pipelines.")
@optgroup.group("Repository Details")
@optgroup.option("--org", "organization", help="Organization URL", required=True)
@optgroup.option("--project", help="Azure DevOps project name", required=True)
@optgroup.group("Azure DevOps Authentication")
@optgroup.option("--token", "personal_access_token", help="Azure DevOps personal access token", envvar="AZURE_DEVOPS_ACCESS_TOKEN", required=True)
def create_work_items(sarif_file, write_logs, organization, project, personal_access_token):
    """Create work items in Azure DevOps for each finding."""
    azure_sarif = AzureSarif()
    azure_sarif.set_metadata(organization, project)
    if write_logs:
        azure_sarif.print_logging_commands()
    azure_sarif.set_auth(personal_access_token)
    azure_sarif.load_from_file(sarif_file)
    azure_sarif.create_work_items()
