from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import AudioPiped
import os

# Get credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Setup clients
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

# Start command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🎶 Hello! I am your custom music bot.\nUse `/play <url>` to play music in a voice chat.")

# Play command
@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Please provide a song URL or file path")

    link = message.text.split(None, 1)[1]
    chat_id = message.chat.id

    try:
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(link)
        )
        await message.reply(f"▶️ Now playing: {link}")
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")

# Run bot
app.start()
pytgcalls.start()
idle()
