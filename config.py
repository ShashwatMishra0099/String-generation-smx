import os

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not (API_ID and API_HASH and BOT_TOKEN):
    raise Exception("API_ID, API_HASH, and BOT_TOKEN must be set in environment variables.")
