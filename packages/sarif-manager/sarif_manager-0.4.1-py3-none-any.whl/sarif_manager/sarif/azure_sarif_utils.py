import sys
import re
from base64 import b64encode

import markdown
import requests
from bs4 import BeautifulSoup


def trim_uuid(input_string: str) -> str:
    """
    Trim UUID from the beginning of a string.
    Handles both hyphenated and non-hyphenated UUIDs.
    """
    # Regex pattern to match a UUID with or without hyphens
    uuid_pattern = r'[a-f0-9]{8}(?:-?[a-f0-9]{4}){3}-?[a-f0-9]{12}'

    # Replace the first occurrence of the UUID and the following hyphen with an empty string
    trimmed_string = re.sub(f'^{uuid_pattern}-?', '', input_string, count=1, flags=re.IGNORECASE)

    return trimmed_string.strip()


def get_azure_headers(pat: str) -> dict:
    """Get headers for the Azure DevOps API."""
    credentials = b64encode(bytes(f":{pat}", 'utf-8')).decode('ascii')
    return {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json-patch+json'
    }


def get_azure_work_items_api_url(organization: str, project: str) -> str:
    return f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Issue?api-version=6.0"


def get_azure_work_item_query_url(organization: str, project: str) -> str:
    return f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=6.0"


def get_existing_work_items(organization: str, project: str, headers: dict, fingerprint: tuple) -> list:
    """Query Azure Boards to check for existing work items with the same fingerprint."""
    # The fingerprint comes as a tuple of (key, value)
    fingerprint_value = fingerprint[1]
    
    # WIQL query needs to be in this specific format
    wiql = {
        "query": f"""SELECT [System.Id]
                    FROM WorkItems
                    WHERE [System.TeamProject] = @project
                    AND [System.Tags] CONTAINS '{fingerprint_value}'"""
    }

    api_url = get_azure_work_item_query_url(organization, project)
    
    # Ensure we have the correct content type for WIQL
    query_headers = headers.copy()
    query_headers['Content-Type'] = 'application/json'
    
    response = requests.post(api_url, headers=query_headers, json=wiql)
    if response.status_code == 200:
        return response.json().get('workItems', [])
    else:
        error_msg = f"Failed to query work items: Status code: {response.status_code}. Response: {response.text}"
        print(error_msg)
        raise RuntimeError(error_msg)


def create_work_item(
        rule_id: str,
        issue_title: str,
        issue_description: str,
        api_url: str,
        headers: dict,
        organization: str = None,
        project: str = None,
        fingerprints: dict = None
):
    """
    Create a single work item in Azure DevOps with URLs converted to HTML links.

    Args:
        rule_id: The ID of the rule that triggered this finding
        issue_title: The title of the work item
        issue_description: The description in markdown format
        api_url: The Azure DevOps API URL (for backward compatibility)
        headers: Request headers including authentication
        organization: Azure DevOps organization name (optional)
        project: Azure DevOps project name (optional)
        fingerprints: Dictionary of fingerprints to check for duplicates (optional)

    Reference: https://learn.microsoft.com/en-us/rest/api/azure/devops/?view=azure-devops-rest-7.2
    """
    # Check for existing work items using fingerprints if all required params are present
    if fingerprints and organization and project:
        for fingerprint in fingerprints.items():
            existing_work_items = get_existing_work_items(organization, project, headers, fingerprint)
            if existing_work_items:
                print(f"Work item already exists for fingerprint: {fingerprint}")
                return

    # Convert Markdown to HTML with extensions for better link handling
    html_description = markdown.markdown(
        issue_description,
        extensions=['extra', 'nl2br']
    )

    # Parse with BeautifulSoup to handle any remaining raw URLs
    soup = BeautifulSoup(html_description, 'html.parser')
    
    # Find text nodes that contain URLs and convert them to links
    for text in soup.find_all(string=True):
        if text.parent.name != 'a':  # Don't process text that's already in a link
            urls = re.finditer(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text.string)
            for url in urls:
                url_text = url.group(0)
                link = soup.new_tag('a', href=url_text)
                link.string = url_text
                text.replace_with(text.replace(url_text, str(link)))

    # Format the HTML nicely
    formatted_description = str(soup)

    # Add fingerprints to tags if provided
    tags = ["Security Vulnerability"]
    if fingerprints:
        tags.extend(str(fp) for fp in fingerprints.values())

    json_data = [
        {"op": "add", "path": "/fields/System.Title", "value": issue_title},
        {"op": "add", "path": "/fields/System.Description", "value": formatted_description},
        {"op": "add", "path": "/fields/System.Tags", "value": "; ".join(tags)}
    ]

    response = requests.post(api_url, headers=headers, json=json_data)
    if response.status_code == 200:
        response_data = response.json()
        html_url = response_data.get('_links', {}).get('html', {}).get('href')
        if html_url:
            print(f"Work item created - {rule_id}: {html_url}")
            return response_data
        else:
            error_msg = f"Failed to get work item URL from response for {rule_id}"
            print(error_msg)
            raise RuntimeError(error_msg)
    else:
        error_msg = f"Failed to create work item: {rule_id}. Status code: {response.status_code}. Response: {response.text}"
        print(error_msg)
        raise RuntimeError(error_msg)
