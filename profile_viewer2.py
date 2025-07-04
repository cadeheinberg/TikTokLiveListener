from playwright.sync_api import sync_playwright, Error

def open_tiktok_profile(page, username: str):
    url = f"https://www.tiktok.com/@{username}"
    try:
        response = page.goto(url, timeout=60000)
    except Error as e:
        # navigation was interrupted by a redirect or other client-side nav
        print(f"[!] Could not navigate to @{username}: {e}")
        return

    # if the server sent back a non-200 (e.g. user not found), bail out
    status = response.status if response else None
    if status != 200:
        print(f"[!] @{username} returned status {status}, skipping…")
        return

    try:
        page.wait_for_selector("img[class*=ImgAvatar]", timeout=15000)
    except Error:
        print(f"[!] Avatar selector not found for @{username}")
        return

    print(f"Opened {url}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # manual login step
        page.goto("https://www.tiktok.com", timeout=60000)
        input("Log in manually in the browser window, then press Enter here…")

        # loop profiles
        while True:
            username = input("Enter TikTok username (without @), or blank to exit: ").strip()
            if not username:
                break
            open_tiktok_profile(page, username)

        browser.close()

if __name__ == "__main__":
    main()
