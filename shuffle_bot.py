from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument
import random

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'
channel_username = 'YOUR_CHANNEL_USERNAME'
count = 100  # Количество треков для отправки

client = TelegramClient('shuffle_session', api_id, api_hash).start(bot_token=bot_token)

async def main():
    print("Сканирую канал...")
    messages = []
    async for msg in client.iter_messages(channel_username, limit=0):
        if msg.media and isinstance(msg.media, MessageMediaDocument) and msg.file.mime_type.startswith("audio"):
            messages.append(msg)

    print(f"Найдено {len(messages)} аудиофайлов.")
    selected = random.sample(messages, k=min(count, len(messages)))

    print("Отправляю в Избранное...")
    for i in range(0, len(selected), 10):
        group = selected[i:i+10]
        files = [msg.media.document for msg in group]
        await client.send_file("me", files)

    print("Готово!")

with client:
    client.loop.run_until_complete(main())
