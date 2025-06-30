from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent, FollowEvent, LikeEvent

client = TikTokLiveClient(
    unique_id="@delightmb",
)

MONEY_PER_DIAMOND = 0.005
running_total_usd = 0.0

async def on_connect(event: ConnectEvent):
    print(f"Connected to @{event.unique_id} (Room ID: {client.room_id}")

async def on_comment(event: CommentEvent):
    print(f"[COMMENT] {event.user.unique_id}: {event.comment}")

async def on_gift(event: GiftEvent):
    global running_total_usd
    
    # Streakable gift & streak is over
    if event.gift.streakable and not event.streaking:
        sender = event.user.unique_id
        count = event.repeat_count
        gift_name = event.gift.name
        diamonds = event.gift.diamond_count
        total_diamonds = count * diamonds
        dollarsEarned = total_diamonds * MONEY_PER_DIAMOND
        running_total_usd += dollarsEarned
        print(f"{sender} sent {count}x \"{gift_name}\" (gift: {total_diamonds} diamonds) (gift: ${dollarsEarned}) (total gifts: ${running_total_usd})")

    # Non-streakable gift
    elif not event.gift.streakable:
        sender = event.user.unique_id
        count = 1
        gift_name = event.gift.name
        diamonds = event.gift.diamond_count
        total_diamonds = count * diamonds
        dollarsEarned = total_diamonds * MONEY_PER_DIAMOND
        running_total_usd += dollarsEarned
        print(f"{sender} sent {count}x \"{gift_name}\" (gift: {total_diamonds} diamonds) (gift: ${dollarsEarned}) (total gifts: ${running_total_usd})")

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
    client.run()