from ..github_api import fetch_ready_items

def test_fetch_ready_items(monkeypatch):
    mock_response = {
        "data": {
            "node": {
                "items": {
                    "nodes": [
                        {
                            "fieldValues": {
                                "nodes": [
                                    {"field": {"name": "Title"}, "text": "Test Title"},
                                    {"field": {"name": "Status"}, "name": "Ready"},
                                    {"field": {"name": "End date"}, "date": "2024-06-07"},
                                    {"field": {"name": "Assignees"}, "users": {"nodes": [{"name": "Assignee 1"}, {"name": "Assignee 2"}]}}
                                ]
                            }
                        }
                    ]
                }
            }
        }
    }

    def mock_post(*args, **kwargs):
        class MockResponse:
            def json(self):
                return mock_response
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)
    
    result = fetch_ready_items()
    assert result == [
    "title: Test Title, end_date: 2024-06-07, assignees: Assignee 1, Assignee 2 期日が今日です！今すぐにやってください。"
]

