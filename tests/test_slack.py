import os
from ..slack import post_slack
from unittest.mock import MagicMock

def test_post_slack(monkeypatch):
    mock_post = MagicMock()
    monkeypatch.setattr("requests.post", mock_post)
    
    messages = [
        "Test message 1",
        "Test message 2"
    ]
    
    post_slack(messages)
    
    # この時点でmock_postが2回呼び出されたことを確認する
    assert mock_post.call_count == 2
    mock_post.assert_any_call(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {os.getenv('SLACK_API_TOKEN')}",
            "Content-Type": "application/json; charset=utf-8"
        },
        json={
            "channel": "random",
            "text": "Test message 1"
        }
    )
    mock_post.assert_any_call(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {os.getenv('SLACK_API_TOKEN')}",
            "Content-Type": "application/json; charset=utf-8"
        },
        json={
            "channel": "random",
            "text": "Test message 2"
        }
    )
