from telethon import TelegramClient, events, Button
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
session_file = os.getenv('SESSION_FILE')  # Path to your session file
source_channel = '@Sodere_Tube'
target_channel = '@SODERE_FILM_ET'

client = TelegramClient(session_file, api_id, api_hash)

# Variable to keep track of counters
button_counters = {
    "like": 0,
    "thumb_up": 0,
    "share": 0
}

# Event handler to listen for new messages in the source channel
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    if event.media:
        print("New message with media detected")
        original_caption = event.message.message
        updated_caption = original_caption.replace('Sodere_Tube', 'SODERE_FILM_ET') if 'Sodere_Tube' in original_caption else original_caption
        buttons = [
            [Button.inline("❤️", b"like"), Button.inline("👍", b"thumb_up"), Button.inline("📤 Share", b"share")]
        ]
        await client.send_file(
            target_channel,
            event.message.media,
            caption=updated_caption,
            buttons=buttons
        )
        print(f"Media sent to {target_channel} with updated caption and inline buttons.")

@client.on(events.CallbackQuery)
async def callback_handler(event):
    callback_data = event.data.decode()
    print(f"Callback received: {callback_data}")
    if callback_data in button_counters:
        button_counters[callback_data] += 1
        await event.answer(f"{callback_data} clicked. Total clicks: {button_counters[callback_data]}")
        if callback_data == "share":
            message = await client.get_messages(source_channel, limit=1)
            if message and message.media:
                await client.send_file(
                    target_channel,
                    message.media,
                    caption="Forwarded media"
                )
                print(f"Media forwarded to {target_channel} upon share button click.")
                await event.answer("Media has been forwarded.")
    else:
        await event.answer("Unknown action")

with client:
    print(f"Listening for new messages in {source_channel}...")
    client.run_until_disconnected()
