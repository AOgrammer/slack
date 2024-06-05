from github_api import fetch_ready_items
from slack import post_slack

if __name__ == "__main__":
    ready_items = fetch_ready_items()
    post_slack(ready_items)
