# Reference
import locale
import datetime
import json
from urllib.request import Request, urlopen


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

# ロケールをシステムのデフォルトに設定
locale.setlocale(locale.LC_TIME, '')

# 現在の日付を取得
today = datetime.date.today()

# 曜日
weekday_name = today.strftime("%A")

# メッセージ
# message = f"こんにちは！今日の日付は{today}です。今日の曜日は{weekday_name}です！"

message = "入力できました！"

if __name__ == "__main__":
    webhook_url = '<https://discord.com/api/webhooks/1244879323643772996/2Lc1dRAjXxHC7_eA5vps8GZQSFopD1ZgqAy4EyzH9Nsf1SUQRXYj0jOKXFmV1xcuit1S>'
    post_discord(message, webhook_url)
