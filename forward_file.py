import os
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
source_channel = '@Sodere_Tube'  # Source channel to listen for new messages
target_channel = '@SODERE_FILM_ET'  # Target channel to forward the file

client = TelegramClient('session_name', api_id, api_hash)

# Variable to keep track of counters
button_counters = {
    "like": 0,
    "thumb_up": 0,
    "share": 0
}

# Event handler to listen for new messages in the source channel
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    if event.media:  # Check if the message contains media (file, photo, video, etc.)
        print("New message with media detected")

        # Get the original caption
        original_caption = event.message.message

        # Replace 'Sodere_Tube' with 'SODERE_FILM_ET'
        updated_caption = original_caption.replace('Sodere_Tube', 'SODERE_FILM_ET') if 'Sodere_Tube' in original_caption else original_caption

        # Define the inline buttons
        buttons = [
            [Button.inline("❤️", b"like"), Button.inline("👍", b"thumb_up"), Button.inline("📤 Share", b"share")]
        ]
        
        # Send the file with the media, updated caption, and inline buttons
        await client.send_file(
            target_channel,
            event.message.media,  # The media (file) from the original message
            caption=updated_caption,  # Use the updated caption
            buttons=buttons
        )
        print(f"Media sent to {target_channel} with updated caption and inline buttons.")

# Event handler to handle callback queries from inline buttons
@client.on(events.CallbackQuery)
async def callback_handler(event):
    # Extract the callback data
    callback_data = event.data.decode()
    print(f"Callback received: {callback_data}")

    if callback_data in button_counters:
        # Increase the counter for the clicked button
        button_counters[callback_data] += 1
        await event.answer(f"{callback_data} clicked. Total clicks: {button_counters[callback_data]}")

        if callback_data == "share":
            # Forward the media from the source channel to the target channel
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

# Start the client and listen for new messages
with client:
    print(f"Listening for new messages in {source_channel}...")
    client.run_until_disconnected()
