import asyncio
from telegram import Bot
from telegram.error import TelegramError

# Telegram bot token
TOKEN = 'YOUR_BOT_TOKEN'

# Function to extract smart contract and social network links
async def extract_info(message):
    # This is a placeholder function. You'll need to implement the actual
    # logic to parse the message and extract relevant information
    smart_contract = None
    social_links = []
    
    # Example logic (adjust based on actual message structure):
    if 'smart contract:' in message.lower():
        smart_contract = message.split('smart contract:')[1].strip().split()[0]
    
    # Look for common social network keywords
    social_networks = ['twitter', 'telegram', 'facebook', 'instagram', 'discord']
    for network in social_networks:
        if network in message.lower():
            # This assumes links are in the format "network: link"
            link = message.lower().split(f'{network}:')[1].strip().split()[0]
            social_links.append((network, link))
    
    return smart_contract, social_links

async def main():
    bot = Bot(TOKEN)
    
    try:
        # Get bot information
        bot_info = await bot.get_me()
        print(f"Bot Name: {bot_info.first_name}")
        print(f"Bot Username: @{bot_info.username}")
        
        # Get updates from the bot
        offset = 0
        while True:
            updates = await bot.get_updates(offset=offset, timeout=30)
            for update in updates:
                if update.message:
                    smart_contract, social_links = await extract_info(update.message.text)
                    
                    if smart_contract:
                        print(f"Smart Contract: {smart_contract}")
                    
                    if social_links:
                        print("Social Network Links:")
                        for network, link in social_links:
                            print(f"{network.capitalize()}: {link}")
                    
                    print("---")
                
                offset = update.update_id + 1
            
            # Add a small delay to avoid hitting rate limits
            await asyncio.sleep(1)
    
    except TelegramError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())