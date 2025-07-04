from playwright.sync_api import sync_playwright

def open_tiktok_profile(page, username: str):
    url = f"https://www.tiktok.com/@{username}"
    page.goto(url, timeout=60000)
    page.wait_for_selector("img[class*=ImgAvatar]", timeout=15000)
    print(f"Opened {url}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # first profile
        open_tiktok_profile(page, "delightmb")

        # # wait 5 seconds before navigating to the next profile
        # page.wait_for_timeout(10000)

        # # navigate to a different profile in the same tab
        # open_tiktok_profile(page, "cade1")

        # page.wait_for_timeout(5000)

        # # navigate to a different profile in the same tab
        # open_tiktok_profile(page, "cade2")

        # keep the browser open until you decide to close
        input("Press Enter to close browser and exit…")
        browser.close()

if __name__ == "__main__":
    main()
