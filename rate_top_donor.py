import sys
import threading
import time
import requests
from collections import defaultdict

from TikTokLive import TikTokLiveClient
from TikTokLive.events import (
    ConnectEvent,
    CommentEvent,
    GiftEvent,
    FollowEvent,
    LikeEvent,
)
from playwright.sync_api import sync_playwright

client = TikTokLiveClient(unique_id="@lolajbunny")

MONEY_PER_DIAMOND = 0.005
gifting_tracker = defaultdict(int)
like_tracker = defaultdict(int)

# How many seconds between reports
INTERVAL_SECONDS = 10

# Event listeners

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
    liker = event.user.unique_id
    like_tracker[liker] += 1
    print(f"[LIKE] {liker} liked the stream (total likes: {like_tracker[liker]})")

client.add_listener(ConnectEvent, on_connect)
client.add_listener(CommentEvent, on_comment)
client.add_listener(GiftEvent, on_gift)
client.add_listener(FollowEvent, on_follow)
client.add_listener(LikeEvent, on_like)

# Profile picture helpers

def get_tiktok_profile_pic(username):
    print(f"get_tiktok_profile_pic: starting for {username}")
    url = f"https://www.tiktok.com/@{username}"
    with sync_playwright() as p:
        print("launching browser")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print(f"navigating to {url}")
        page.goto(url, timeout=60000)
        print("waiting for avatar selector")
        page.wait_for_selector("img[class*=ImgAvatar]", timeout=30000)

        img = page.query_selector("img[class*=ImgAvatar]")
        if not img:
            browser.close()
            raise Exception("Profile picture element not found")

        print("extracting src")
        src = img.get_attribute("src")

        context.close()
        browser.close()
        print(f"got profile pic URL: {src}")
        return src

def download_image(image_url, filename):
    print(f"download_image: fetching {image_url}")
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"saved image as {filename}")
    else:
        raise Exception(f"Failed to download image: HTTP {response.status_code}")

# Top-gifter/liker loop

def process_top_user(user):
    try:
        pic_url = get_tiktok_profile_pic(user)
        download_image(pic_url, f"{user}.jpg")
    except Exception as e:
        print(f"Error fetching profile picture for {user}: {e}")

def track_top_gifter_loop():
    print("Starting top-gifter/liker loop...")
    while True:
        # countdown
        for remaining in range(INTERVAL_SECONDS, 0, -1):
            print(f"Next check in {remaining} seconds", end="\r")
            time.sleep(1)
        print()  # move to next line after countdown

        if gifting_tracker:
            user, total = max(gifting_tracker.items(), key=lambda kv: kv[1])
            print(f"Top gifter: {user} with {total} diamonds")
        elif like_tracker:
            user, total = max(like_tracker.items(), key=lambda kv: kv[1])
            print(f"No gifts; top liker: {user} with {total} likes")
        else:
            print("No gifts or likes this round.")
            gifting_tracker.clear()
            like_tracker.clear()
            continue

        threading.Thread(target=process_top_user, args=(user,), daemon=True).start()

        gifting_tracker.clear()
        like_tracker.clear()

# Entry point

if __name__ == "__main__":
    threading.Thread(target=track_top_gifter_loop, daemon=True).start()
    client.run()
