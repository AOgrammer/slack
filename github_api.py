import os
import requests
from datetime import datetime

def fetch_ready_items():
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {os.getenv('MY_GITHUB_TOKEN')}",
        "Content-Type": "application/json"
    }

    query = """
    {
      node(id: "PVT_kwHOAOY4Ws4AifCH") {
        ... on ProjectV2 {
          items(first: 30) {
            nodes {
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
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                    name
                  }
                  ... on ProjectV2ItemFieldDateValue {
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                    date
                  }
                  ... on ProjectV2ItemFieldUserValue {
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                    users(first: 3) {
                      nodes {
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
    
    ready_items = []
    today = datetime.today().date()

    for item in data["data"]["node"]["items"]["nodes"]:
        title = ""
        status = ""
        end_date = ""
        assignees = []

        # カードのフィールド一覧で表示したいフィールド（title, status, end_date, assignees）だけを抽出
        for field in item["fieldValues"]["nodes"]:
            if field["field"]["name"] == "Title":
                title = field["text"]
            if field["field"]["name"] == "Status":
                status = field["name"]
            if field["field"]["name"] == "End date":
                end_date = field["date"]
            if field["field"]["name"] == "Assignees":
                assignees = [user["name"] for user in field["users"]["nodes"]]

        # カードのステータスが、Readyのものだけ結果の配列に追加 
        if status == "Ready":
            message = f"title: {title}, end_date: {end_date}, assignees: {', '.join(assignees)}"
            if end_date:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                delta_days = (end_date_obj - today).days

                if delta_days > 0 and delta_days <= 2:
                    message += f" 期日が近いです。残り{delta_days}日です。"
                elif delta_days == 0:
                    message += " 期日が今日です！今すぐにやってください。"
                elif delta_days < 0:
                    message += f" 期日が{abs(delta_days)}日過ぎています！"
            
            ready_items.append(message)

    return ready_items
