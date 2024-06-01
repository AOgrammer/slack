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
    for field in item["fieldValues"]["nodes"]:
        if field["field"]["name"] == "Title":
            title = field["text"]
        if field["field"]["name"] == "Status":
            status = field["name"]
    if status == "Ready":
        ready_items.append({"id": item["id"], "title": title, "status": status})


# 結果を表示
for item in ready_items:
    print(f"ID: {item['id']}, Title: {item['title']}, Status: {item['status']}")


def post_discord(message: str, webhook_url: str):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (private use) Python-urllib/3.10",
    }
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
    post_discord(message, webhook_url)
