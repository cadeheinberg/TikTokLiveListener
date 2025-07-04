from playwright.sync_api import sync_playwright
import requests

def get_tiktok_profile_pic(username):
    url = f"https://www.tiktok.com/@{username}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Create incognito context (this is what makes it private)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_selector("img[class*=ImgAvatar]", timeout=15000)
        
        img = page.query_selector("img[class*=ImgAvatar]")
        if not img:
            raise Exception("Profile picture not found")

        src = img.get_attribute("src")
        print("Profile pic URL:", src)

        # Cleanup
        context.close()
        browser.close()
        return src

def download_image(image_url, filename="profile.jpg"):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Saved image as {filename}")
    else:
        raise Exception(f"Failed to download image: {response.status_code}")

# Run
pic_url = get_tiktok_profile_pic("delightmb")
download_image(pic_url)
