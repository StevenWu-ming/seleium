import datetime
import json

def save_random_data_to_json(data, filename="random_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def generate_random_username():
    timestamp = datetime.datetime.now().strftime("%y%m%d%H%M%S")  # 取 2 位數年份
    random_username = f"QA_M1_CP{timestamp}"
    # 儲存到 JSON
    save_random_data_to_json({"random_username": random_username})
    return random_username

# 測試
print(generate_random_username())
