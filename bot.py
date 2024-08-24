import requests
import telebot
from telegraph import Telegraph

# Initialize bot with your Telegram bot token
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Initialize Telegraph client
telegraph = Telegraph()
telegraph.create_account(short_name='bot')

# Function to fetch search results
def fetch_search_results(query):
    url = f"https://scloud.starkflix.cloud/search?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to create Telegraph page
def create_telegraph_page(title, content):
    response = telegraph.create_page(
        title=title,
        html_content=content
    )
    return response['url']

# Command to handle the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_message = (
        "👋 Welcome to the Search Bot!\n\n"
        "You can search for files by using the /s command followed by your query.\n\n"
        "For example: /s Kalki 2898 AD\n\n"
        "I'll provide you with a Telegraph page containing the search results. Enjoy!"
    )
    bot.send_message(message.chat.id, welcome_message)

# Command to handle search queries from /s command
@bot.message_handler(commands=['s'])
def handle_search(message):
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "Please provide a search query after the /s command.")
        return

    query = message.text.split(maxsplit=1)[1]  # Get the search query after /s command
    results = fetch_search_results(query)

    if results:
        # Format content for Telegraph page
        content = ""
        for result in results:
            content += f"<b>Title:</b> {result['title']}<br>"
            content += f"<b>Size:</b> {result['size']}<br>"
            content += f"<b>Direct Link:</b> <a href='https://scloud.starkflix.cloud/file/{result['id']}'>Download</a><br><br>"

        # Create Telegraph page
        page_url = create_telegraph_page(query, content)

        # Send the Telegraph page link to the user
        bot.send_message(message.chat.id, f"Search results for '{query}': {page_url}")
    else:
        bot.send_message(message.chat.id, "No results found or there was an error fetching the data.")

# Start the bot
bot.polling()
