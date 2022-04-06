from ghapi.all import GhApi
import os
from notion_client import Client
from dataclasses import dataclass
from . import notion


def retrieve_open_github_issues(api):
    gh_issues = api.issues.list_for_repo(owner='SwissDataScienceCenter', repo='POC', assignee='lokijuhy')
    return gh_issues


def retrieve_notion_github_tasks(notion_client, db_id):
    # Retrieve Notion tasks marked as GitHub issues (contain '#')

    task_query_results = notion_client.databases.query(
        **{
            "database_id": db_id,
            "filter": {
                "property": "Name",
                "text": {
                    "contains": "#"
                },
            },
        }
    )

    # projects_query_results = noexition_client.databases.query(
    #     **{
    #         "database_id": projects_db_id,
    #     }
    # )

    tasks_json = task_query_results['results']
    tasks = [notion.model.Task.from_json(j) for j in tasks_json]
    return tasks


def identify_issues_to_sync_to_notion(gh_issues, notion_tasks):
    open_gh_issue_numbers = [i.number for i in gh_issues]
    existing_notion_tasks_numbers = [t.number for t in notion_tasks]
    issue_numbers_to_add = list(set(open_gh_issue_numbers).difference(set(existing_notion_tasks_numbers)))
    issues_to_add = [i for i in gh_issues if i.number in issue_numbers_to_add]
    return issues_to_add


def add_issues_to_notion(notion_client, db_id, issues):
    for i in issues:
        print(f"Syncing #{i.number} {i.title}...")
        response = notion.interface.add_task_to_notion(notion_client, db_id, i.number, i.title)


def main():
    gh_client = GhApi()
    notion_client = Client(auth=os.environ["NOTION_GITHUB_SYNC_TOKEN"])
    tasks_db_id = 'b09ea507-56c4-4b01-8bd2-94102e5db7ac'
    # projects_db_id = '810c333ac6c44f5ab49f9f18e2412f3c'

    gh_issues = retrieve_open_github_issues(gh_client)
    notion_tasks = retrieve_notion_github_tasks(notion_client, tasks_db_id)
    issues_to_add = identify_issues_to_sync_to_notion(gh_issues, notion_tasks)

    if len(issues_to_add) == 0:
        print('Up to date!')
        return

    add_issues_to_notion(notion_client, tasks_db_id, issues_to_add)


if __name__ == '__main__':
    main()
