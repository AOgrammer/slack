import requests
import os

# 環境変数からSlackトークンを取得
TOKEN = os.getenv("SLACK_API_TOKEN")

# 投稿先のチャンネル名を設定
CHANNEL = "random"

def post_slack(messages: list):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    for message in messages:
        data = {
            "channel": CHANNEL,
            "text": message
        }
        requests.post(url, headers=headers, json=data)