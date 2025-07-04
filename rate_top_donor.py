import asyncio
import time
import requests
from collections import defaultdict

from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent, FollowEvent, LikeEvent
from playwright.sync_api import sync_playwright

client = TikTokLiveClient(unique_id="@lolajbunny")

MONEY_PER_DIAMOND = 0.005
gifting_tracker = defaultdict(int)  # Tracks total diamonds per user

def get_tiktok_profile_pic(username):
    url = f"https://www.tiktok.com/@{username}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_selector("img[class*=ImgAvatar]", timeout=15000)
        img = page.query_selector("img[class*=ImgAvatar]")
        if not img:
            raise Exception("Profile picture not found")

        src = img.get_attribute("src")

        context.close()
        browser.close()
        return src

def download_image(image_url, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Saved image as {filename}")
    else:
        raise Exception(f"Failed to download image: {response.status_code}")

async def track_top_gifter_loop():
    while True:
        await asyncio.sleep(180)  # Wait 3 minutes
        if not gifting_tracker:
            print("No gifts this round.")
            continue
        top_user = max(gifting_tracker.items(), key=lambda x: x[1])[0]
        print(f"Top gifter this round: {top_user} with {gifting_tracker[top_user]} diamonds")
        try:
            pic_url = get_tiktok_profile_pic(top_user)
            download_image(pic_url, f"{top_user}.jpg")
        except Exception as e:
            print(f"Error getting profile picture: {e}")
        gifting_tracker.clear()

async def on_connect(event: ConnectEvent):
    print(f"Connected to @{event.unique_id} (Room ID: {client.room_id})")

async def on_comment(event: CommentEvent):
    print(f"[COMMENT] {event.user.unique_id}: {event.comment}")

async def on_gift(event: GiftEvent):
    if event.gift.streakable and not event.streaking:
        diamonds = event.repeat_count * event.gift.diamond_count
    elif not event.gift.streakable:
        diamonds = event.gift.diamond_count
    else:
        return
    sender = event.user.unique_id
    gifting_tracker[sender] += diamonds
    print(f"[GIFT] {sender} sent {diamonds} diamonds (total: {gifting_tracker[sender]})")

async def on_follow(event: FollowEvent):
    print(f"[FOLLOW] {event.user.unique_id} just followed!")

async def on_like(event: LikeEvent):
    print(f"[LIKE] {event.user.unique_id} liked the stream")

client.add_listener(ConnectEvent, on_connect)
client.add_listener(CommentEvent, on_comment)
client.add_listener(GiftEvent, on_gift)
client.add_listener(FollowEvent, on_follow)
client.add_listener(LikeEvent, on_like)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(track_top_gifter_loop())
    loop.run_until_complete(client.run())
