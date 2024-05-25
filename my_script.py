import datetime

# 今日の日付を取得
today = datetime.date.today()

# 曜日を取得 (月曜日=0, 日曜日=6)
weekday_number = today.weekday()

# 日本語の曜日名のリスト
weekday_japense = ["月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日"]

# 今日の日本語の曜日名を取得
today_weekday_japanese = weekday_japense[weekday_number]

print("こんにちは！")
print(f"今日の日付は{today}")
print(f"曜日は {today_weekday_japanese}です！")
