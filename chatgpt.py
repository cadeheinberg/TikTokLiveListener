from playwright.sync_api import sync_playwright, Error

def send_to_chatgpt(page, message: str):
    # wait for the visible, contenteditable chat box
    editor = page.wait_for_selector('div[role="textbox"]', timeout=60000)
    editor.click()
    # type your message
    page.keyboard.type(message)
    # hit Enter to send
    page.keyboard.press("Enter")
    # wait for ChatGPT's reply to appear
    page.wait_for_selector('div.markdown', timeout=60000)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 1. Go to ChatGPT and manually log in
        page.goto("https://chat.openai.com/", timeout=60000)
        input("Log in in the browser window, then press Enter here…")

        # 2. Make sure the chat box is ready
        page.wait_for_selector('div[role="textbox"]', timeout=60000)
        print("✅ ChatGPT is ready. Type messages below (type 'exit' to quit).")

        # 3. Loop: read from console → send → wait
        while True:
            msg = input("> ").strip()
            if msg.lower() == "exit":
                break
            if not msg:
                continue
            try:
                send_to_chatgpt(page, msg)
            except Error as e:
                print(f"[!] Error sending message: {e}")
                break

        browser.close()

if __name__ == "__main__":
    main()
