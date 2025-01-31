import click
from click_option_group import optgroup
from sarif_manager.sarif.slack_sarif import SlackSarif


@click.group("slack")
def slack():
    """Manage Slack notifications."""


@slack.command("send", help="Send SARIF findings to a Slack channel.")
@click.argument("sarif-file", type=click.Path(exists=True))
@optgroup.group("Slack Details")
@optgroup.option("--channel", help="Slack channel ID", required=True, envvar="SLACK_CHANNEL")
@optgroup.option("--token", help="Slack bot token", required=True, envvar="SLACK_BOT_TOKEN")
def send_to_slack(sarif_file, channel, token):
    """Send SARIF findings to a Slack channel."""
    slack_sarif = SlackSarif()
    slack_sarif.set_auth(token)
    slack_sarif.set_channel(channel)
    slack_sarif.load_from_file(sarif_file)
    response = slack_sarif.send_to_slack()
    if response and response["ok"]:
        click.echo("Successfully sent findings to Slack!")
    else:
        click.echo("Failed to send findings to Slack", err=True)

