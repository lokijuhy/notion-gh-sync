
def add_task_to_notion(client, db_id, number, name):
    notion_task_name = f"#{number} {name}"
    response = client.pages.create(
        **{
            "parent": {
                "database_id": db_id,
            },
            "properties": {
                "Name": {
                    'title': [
                        {
                            'text': {
                                'content': notion_task_name,
                            },
                        },
                    ],
                },
                'Status': {
                    'id': 'd~P%5E',
                    'type': 'select',
                    'select': {
                        'id': '9c1fdaae-c09e-4f4d-9ead-374ebbfa06eb',
                        'name': 'Queued',
                        'color': 'yellow',
                    }
                },
                'Tags': {
                    'id': 'yQ%3Bs',
                    'type': 'multi_select',
                    'multi_select': [
                        {
                            'id': '433d7f20-246e-42d4-8849-97834f188f53',
                            'name': 'GitHub',
                            'color': 'purple'
                        }
                    ]
                },

            },
        }
    )
    return response
