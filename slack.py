import requests
import os
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout

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
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
        except ConnectionError as ce:
            print("Connection Error:", ce)
        except HTTPError as he:
            print("HTTEP Error:", he)
        except Timeout as te:
            print("Timeout Error:", te)
        except RequestException as re:
            print("Error:", re)