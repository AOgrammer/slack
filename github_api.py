import os
import requests

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

    for item in data["data"]["node"]["items"]["nodes"]:
        title = ""
        status = ""
        end_date = ""
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
                "title": title,
                "end_date": end_date,
                "assignees": assignees
            })

    return ready_items
