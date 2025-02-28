import os
import logging
from binance.client import Client
from binance.enums import ORDER_TYPE_MARKET, SIDE_BUY, SIDE_SELL
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

# Configure logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Binance API keys (replace with your keys)
BINANCE_API_KEY = 'dR20qb0XFV8Cy8Qg0MzGpV85fAlvsSzhLmnQ7dEqLiM7UKp7QjL3mPaNXUjamzWuy'
BINANCE_API_SECRET = 'dR20qb0XFV8Cy8Qg0MzGpV85fAlvsSzhLmnQ7dEqLiM7UKp7QjL3mPaNXUjamzWu'

# Initialize Binance client
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# Telegram bot token (replace with your bot token)
TELEGRAM_TOKEN = '7842190123:AAHfqrOOz-kGiHRu5UsKv3SBQH81Jh5fF_0'

# Variables for market thresholds
max_price = None
min_price = None
symbol = "BTCUSDT"  # Default trading pair

def start(update: Update, context: CallbackContext):
    """Send a welcome message and options to the user."""
    keyboard = [
        [InlineKeyboardButton("Start", callback_data='start_trading')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Dobrоgo dnya! This is Crypto Bot. To begin, click Start.", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    """Handle button presses."""
    query = update.callback_query
    query.answer()

    if query.data == 'start_trading':
        query.edit_message_text(text="Please enter the maximum market price:")
        context.user_data['next_step'] = 'set_max_price'

def handle_message(update: Update, context: CallbackContext):
    """Handle text messages from the user."""
    global max_price, min_price, symbol

    user_input = update.message.text

    if 'next_step' in context.user_data:
        next_step = context.user_data['next_step']

        if next_step == 'set_max_price':
            try:
                max_price = float(user_input)
                update.message.reply_text(f"Maximum price set to {max_price}. Now, enter the minimum market price:")
                context.user_data['next_step'] = 'set_min_price'
            except ValueError:
                update.message.reply_text("Invalid number. Please enter a valid maximum price.")

        elif next_step == 'set_min_price':
            try:
                min_price = float(user_input)
                update.message.reply_text(f"Minimum price set to {min_price}. Trading will now begin.")
                context.user_data['next_step'] = None
                start_trading(update, context)
            except ValueError:
                update.message.reply_text("Invalid number. Please enter a valid minimum price.")


def start_trading(update: Update, context: CallbackContext):
    """Start monitoring the market and perform trading."""
    global max_price, min_price, symbol

    update.message.reply_text(f"Monitoring market for {symbol}. Maximum: {max_price}, Minimum: {min_price}")

    while True:
        try:
            ticker = client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker['price'])
            logger.info(f"Current price of {symbol}: {current_price}")

            if current_price >= max_price:
                # Sell order
                order = client.create_order(
                    symbol=symbol,
                    side=SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=0.001  # Replace with your desired quantity
                )
                logger.info(f"Sold at {current_price}: {order}")
                update.message.reply_text(f"Sold {symbol} at {current_price}")
                break

            elif current_price <= min_price:
                # Buy order
                order = client.create_order(
                    symbol=symbol,
                    side=SIDE_BUY,
                    type=ORDER_TYPE_MARKET,
                    quantity=0.001  # Replace with your desired quantity
                )
                logger.info(f"Bought at {current_price}: {order}")
                update.message.reply_text(f"Bought {symbol} at {current_price}")
                break

        except Exception as e:
            logger.error(f"Error: {e}")


def main():
    """Start the bot."""
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
