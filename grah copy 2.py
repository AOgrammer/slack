import os
import requests
import json
from urllib.request import Request, urlopen

# GitHub APIのエンドポイント
url = "https://api.github.com/graphql"
headers = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",  # 環境変数からトークンを取得
    "Content-Type": "application/json"
}

# GraphQLクエリ
query = """
{
  user(login: "AOgrammer") {
    projectV2(number: 2) {
      id
      items(first: 100) {
        nodes {
          id
          fieldValues(first: 20) {
            nodes {
              ... on ProjectV2ItemFieldTextValue {
                field {
                  ... on ProjectV2FieldCommon {
                    name
                  }
                }
                text
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field {
                  ... on ProjectV2FieldCommon {
                    name
                  }
                }
              }
              ... on ProjectV2ItemFieldUserValue {
                users(first: 3) {
                  nodes {
                    id
                    login
                    name
                  }
                }
                field {
                  ... on ProjectV2FieldCommon {
                    id
                    dataType
                    name
                  }
                }
              }
              ... on ProjectV2ItemFieldDateValue {
                date
                field {
                  ... on ProjectV2FieldCommon {
                    id
                    dataType
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

response = requests.post(url, headers=headers, json={"query": query})
data = response.json()

# "Ready" ステータスの項目を抽出
ready_items = []

for item in data["data"]["user"]["projectV2"]["items"]["nodes"]:
    title = None
    status = None
    end_date = None
    assignees = []
    for field in item["fieldValues"]["nodes"]:
        if field["field"]["name"] == "Title":
            title = field["text"]
        if field["field"]["name"] == "Status":
            status = field["name"]
        if field["field"]["name"] == "End date":
            end_date = field["date"]
        if field["field"]["name"] == "Assignees":
            assignees = [user["name"] for user in field["users"]["nodes"]]
    if status == "Ready":
        ready_items.append({
            "id": item["id"],
            "title": title,
            "end_date": end_date,
            "assignees": assignees
        })

# メッセージを作成
messages = []
for item in ready_items:
    assignees_str = ', '.join(item['assignees'])
    message = f"Title: {item['title']}, End Date: {item['end_date']}, Assignees: {assignees_str}"
    messages.append(message)

# Discordに投稿
def post_discord(messages: list, webhook_url: str):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (private use) Python-urllib/3.10",
    }
    for message in messages:
        data = {"content": message}
        request = Request(
            webhook_url,
            data=json.dumps(data).encode(),
            headers=headers,
        )

        with urlopen(request) as res:
            assert res.getcode() == 204

if __name__ == "__main__":
    webhook_url = '<https://discord.com/api/webhooks/1244879323643772996/2Lc1dRAjXxHC7_eA5vps8GZQSFopD1ZgqAy4EyzH9Nsf1SUQRXYj0jOKXFmV1xcuit1S>'
    post_discord(messages, webhook_url)
