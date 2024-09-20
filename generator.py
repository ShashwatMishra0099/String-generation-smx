import logging
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, AccessTokenInvalid
import config

logging.basicConfig(level=logging.INFO)

app = Client(
    "string_session_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

@app.on_message(filters.private & filters.command("start"))
async def start(bot, msg):
    await bot.send_message(
        msg.chat.id,
        "Welcome! Click the button below to generate your Pyrogram string session.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Generate", callback_data="generate")]])
    )

@app.on_callback_query(filters.data("generate"))
async def generate_callback(bot, callback_query):
    await callback_query.message.reply("Please send your phone number in the format: +91 1234567890")
    await bot.ask(callback_query.from_user.id, "Please send your phone number:", filters=filters.text)

@app.on_message(filters.private & ~filters.forwarded & filters.text)
async def handle_phone_number(_, msg):
    phone_number = msg.text
    await msg.reply("Sending OTP...")
    
    try:
        async with Client(":memory:", api_id=config.API_ID, api_hash=config.API_HASH) as client:
            code = await client.send_code_request(phone_number)
            otp_msg = await bot.ask(msg.chat.id, "Please enter the OTP sent to your phone:")
            await client.sign_in(phone_number, otp_msg.text)
            string_session = await client.export_session_string()
            await msg.reply(f"Your Pyrogram string session is:\n`{string_session}`", quote=True)
    except Exception as e:
        await msg.reply(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        app.start()
        print("Bot started successfully!")
        idle()
    except (ApiIdInvalid, AccessTokenInvalid):
        print("Invalid API ID or Access Token.")
    finally:
        app.stop()
        print("Bot stopped.")
