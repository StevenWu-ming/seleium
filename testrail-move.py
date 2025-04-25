import requests

# ======= 請替換下列資訊 =======
BASE_URL = "https://gorun.testrail.io"
USERNAME = "Est@intellianalyze.com"
API_KEY = "XhqyRjae2rZMX18Fo0z5-GnkbFo3pzbAhW.JgzWcb"

SOURCE_PROJECT_ID = 2
SOURCE_SUITE_ID = 1  # 從這個 Suite 匯出

TARGET_PROJECT_ID = 10
# ============================

session = requests.Session()
session.auth = (USERNAME, API_KEY)
headers = {"Content-Type": "application/json"}


def get_sections(project_id, suite_id):
    url = f"{BASE_URL}/index.php?/api/v2/get_sections/{project_id}&suite_id={suite_id}"
    res = session.get(url, headers=headers)
    print("⬇️ get_sections 回傳（前 200 字）:", res.text[:200])  # 原始輸出除錯
    res.raise_for_status()
    return res.json().get("sections", [])  # ← ✅ 加這行避免錯誤


def get_cases(project_id, section_id, suite_id):
    url = f"{BASE_URL}/index.php?/api/v2/get_cases/{project_id}&suite_id={suite_id}&section_id={section_id}"
    res = session.get(url, headers=headers)
    print(f"⬇️ get_cases 回傳內容 (前 200 字): {res.text[:200]}")
    res.raise_for_status()
    return res.json().get("cases", [])  # ✅ 加上 .get("cases")



def add_section(project_id, name, parent_id=None):
    url = f"{BASE_URL}/index.php?/api/v2/add_section/{project_id}"
    data = {"name": name}
    if parent_id:
        data["parent_id"] = parent_id
    res = session.post(url, headers=headers, json=data)
    res.raise_for_status()
    return res.json()


def add_case(section_id, case_data):
    url = f"{BASE_URL}/index.php?/api/v2/add_case/{section_id}"
    res = session.post(url, headers=headers, json=case_data)
    res.raise_for_status()
    return res.json()


def migrate_cases():
    print("🚀 開始擷取來源區段與用例...")

    sections = get_sections(SOURCE_PROJECT_ID, SOURCE_SUITE_ID)
    print(f"📁 擷取成功，共 {len(sections)} 個區段")

    section_map = {}

    for section in sections:
        try:
            # 轉換父節點 ID
            original_parent_id = section.get("parent_id")
            parent_id = section_map.get(original_parent_id) if original_parent_id else None

            # 新增目標專案的區段
            new_section = add_section(TARGET_PROJECT_ID, section["name"], parent_id=parent_id)
            section_map[section["id"]] = new_section["id"]

            print(f"  ➕ 區段：{section['name']}（來源 ID: {section['id']}）→ 新 ID: {new_section['id']})")

            # 匯入該區段下所有 test cases
            cases = get_cases(SOURCE_PROJECT_ID, section["id"], SOURCE_SUITE_ID)
            print(f"    ➤ 發現 {len(cases)} 個用例，開始匯入...")

            for case in cases:
                if not isinstance(case, dict):
                    print("⚠️ 異常 case 資料型別：", type(case), case)
                    continue  # 跳過這筆不是 dict 的 case

                case_data = {
                    "title": case["title"],
                    "type_id": case.get("type_id", 1),
                    "priority_id": case.get("priority_id", 2),
                    "refs": case.get("refs", ""),
                    "custom_steps": case.get("custom_steps", ""),
                    "custom_expected": case.get("custom_expected", "")
                }
                add_case(new_section["id"], case_data)

        except Exception as e:
            print(f"⚠️ 區段 {section.get('name', '未知')} 發生錯誤：{e}")

    print("✅ 所有區段與用例匯入完成！")




if __name__ == "__main__":
    migrate_cases()
