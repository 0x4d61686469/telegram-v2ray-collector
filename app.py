import asyncio
import re
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
import socks
import os

# --- CONFIGURATION ---
API_ID = os.environ.get("tel_API_ID")         
API_HASH = os.environ.get("tel_API_HASH")  
SESSION_NAME = 'telegram_config_scraper'  
OUTPUT_FILE = 'extracted_configs.txt'
HOURS_LIMIT = 8

PROXY = (socks.SOCKS5, '127.0.0.1', 10808) 
CONFIG_REGEX = r'(vless://[^\s]+|vmess://[^\s]+)'

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH, proxy=PROXY)
    await client.start()
    print("Successfully logged into Telegram!")

    time_threshold = datetime.now(timezone.utc) - timedelta(hours=HOURS_LIMIT)
    print(f"Searching globally for messages posted after: {time_threshold.strftime('%Y-%m-%d %H:%M:%S UTC')}")

    extracted_configs = set()
    
    # We will run global searches for both prefixes
    search_queries = ['vless://', 'vmess://']

    for query in search_queries:
        print(f"Searching globally for query: '{query}'...")
        
        # client.iter_messages with no entity ID searches GLOBAL across all your joined chats
        async for message in client.iter_messages(None, search=query, limit=500):
            # Because global search results come roughly in reverse chronological order,
            # we can skip older messages, but note: global search order isn't perfectly strict,
            # so we check every message returned in the limit.
            if message.date < time_threshold:
                continue
            
            if message.text:
                matches = re.findall(CONFIG_REGEX, message.text)
                for config in matches:
                    extracted_configs.add(config.strip())

    # Save findings
    if extracted_configs:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for config in extracted_configs:
                f.write(f"{config}\n")
        print(f"\nDone! Successfully extracted {len(extracted_configs)} unique configs to '{OUTPUT_FILE}'.")
    else:
        print("\nNo matching configs found in the last 4 hours.")

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())