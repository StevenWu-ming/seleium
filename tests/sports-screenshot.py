
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

USERNAME = "cooper001"
PASSWORD = "1234Qwer"

sports_pages = [
    {"name": "SoftswissSport", "url": "https://uat-newplatform.mxsyl.com/zh-cn/play/SoftswissSport-1/All"},
    {"name": "PinnacleSport", "url": "https://uat-newplatform.mxsyl.com/zh-cn/play/PinnacleSport-1/All"},
    {"name": "FBSport", "url": "https://uat-newplatform.mxsyl.com/zh-cn/play/FBSport-1/All"},
    {"name": "SaBaSport", "url": "https://uat-newplatform.mxsyl.com/zh-cn/play/SaBaSport-1/All"},
    {"name": "SBO", "url": "https://uat-newplatform.mxsyl.com/zh-cn/play/SBOSport-1/All"},
    {"name": "PM", "url": "https://uat-newplatform.mxsyl.com/zh-cn/play/OBSport-1"},
    {"name": "IMSport", "url": "https://uat-newplatform.mxsyl.com/zh-cn/play/IMSport-1/All"},
]

screenshot_dir = Path("screenshots")
screenshot_dir.mkdir(exist_ok=True)

async def login(page):
    print("🔒 執行登入流程")
    await page.goto("https://uat-newplatform.mxsyl.com/zh-cn/login", timeout=60000)
    await page.fill("//input[@maxlength='18']", USERNAME)
    await page.fill("//input[@type='password']", PASSWORD)
    await page.click("//button[contains(text(), '登录')]")
    await page.wait_for_timeout(3000)
    print("✅ 登入成功或已進入主頁")

async def capture_screenshot_async(playwright, context, sport):
    name = sport["name"]
    url = sport["url"]
    page = await context.new_page()
    print(f"\n⏳ 開始導航: {name} - {url}")

    try:
        try:
            await page.goto(url, timeout=90000, wait_until="load")
        except PlaywrightTimeoutError:
            print(f"⚠️ {name} 初次 timeout，改用 domcontentloaded 再試")
            await page.goto(url, timeout=90000, wait_until="domcontentloaded")

        # 等待 iframe 出現
        await page.wait_for_selector("iframe", timeout=15000, state="visible")
        iframe_element = await page.query_selector("iframe")

        # 進入 iframe
        frame = await iframe_element.content_frame()
        if not frame:
            return f"{name}: ❌ 無法取得 iframe 內容"

        print(f"🔍 等待 iframe 中真正的主內容載入...")

        try:
            # 這裡請根據實際頁面調整 selector，例如 `.main-content` 或 `.sports-container`
            await frame.wait_for_selector(".sports-wrapper, .main-content", timeout=20000, state="visible")
        except PlaywrightTimeoutError:
            print("⚠️ 內容載入逾時，延長等待時間")
            await frame.wait_for_timeout(5000)  # 最後保底等一點時間

        # 確認 iframe 有大小才截圖
        box = await iframe_element.bounding_box()
        if not box or box['width'] == 0 or box['height'] == 0:
            return f"{name}: ❌ iframe 尺寸為 0，可能尚未顯示"

        path = screenshot_dir / f"{name}.png"
        await iframe_element.screenshot(path=str(path))
        print(f"📸 已儲存 {name} 畫面至 {path}")
        return f"{name}: ✅ 擷取成功"

    except Exception as e:
        return f"{name}: ❌ 錯誤: {str(e)}"
    finally:
        await page.close()


async def run_all():
    print("🧹 清除上次截圖")
    for file in screenshot_dir.glob("*.png"):
        try:
            file.unlink()
            print(f"🗑️ 刪除: {file.name}")
        except Exception as e:
            print(f"⚠️ 無法刪除 {file.name}: {e}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await login(page)
        await page.close()

        tasks = [capture_screenshot_async(p, context, sport) for sport in sports_pages]
        results = await asyncio.gather(*tasks)

        print("\n📋 結果總結：")
        for r in results:
            print(r)

        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_all())
