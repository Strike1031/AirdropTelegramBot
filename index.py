# start
import sys

import os
from dotenv import load_dotenv
import requests
import httpx
# end

load_dotenv()

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update)

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import platform
import asyncio

# States
SOL_ADDRESS_STATE, END_STATE = range(2)

TELEGRAM_BOT_TOKEN = os.environ.get('BOT_TOKEN')
# file path to save user infos
FILE_PATH = 'file/report.xlsx'

# variables
users = {}
group_chat_id = 0

class UserInformation:
    def __init__(self, userId, userName, twitterName, solAddress, airdropBalance, referralBalance, referralCount):
        self.userId = userId
        self.userName = userName
        self.twitterName = twitterName
        self.solAddress = solAddress
        self.airdropBalance = airdropBalance
        self.referralBalance = referralBalance
        self.referralCount = referralCount
        
        
# functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send message on `/start`."""

    # Get user that sent /start and log his name
    username = update.effective_user.username
    user_id = update.effective_user.id
    args = context.args
    keyboard = [
            [InlineKeyboardButton("Join Airdrop", callback_data='airdropContent')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = (
        f"""Hello, {username}! I am your friendly GIKO Airdrop Bot.
        
    ✅Please complete all the tasks and submit details correctly to be eligible for the airdrop
    
    💵 Total Reward: 7,256,928,346.29 $GIKO ($50,000,000.00) For All
    
    💲 Reward: 15000 $GIKO (~$100)
    🏆 Refferal: 7500 $GIKO (~50)
    
    🐱GIKO is best a meme coin. It's time to Make GIKO great.
    
    Click "Join Airdrop" to proceed""")

    if args and args[0].startswith('r'):
        referrer_id = int(args[0][1:])  # Extract referrer ID
        if referrer_id in users and users[referrer_id].referralCount < 5:
            users[referrer_id].referralCount += 1
            users[referrer_id].referralBalance += 7500
            context.bot.send_message(chat_id=referrer_id, text=f"ℹ️ User has joined the bot using your referral link.\n\nTotal referrals: {users[referrer_id].referralCount}.")
        else:
            await update.message.reply_text("Referral limit reached for this user.")
            
    if user_id not in users:
        users[user_id] = UserInformation(user_id, username, "", "", 15000, 0, 0)
        
    await update.message.reply_html(message_text, reply_markup=reply_markup)

async def handle_airdropContent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = (
        f"""🐱 Complete Those Task to Join GIKO World:
        
        🔷 Join GIKO <a href="http://t.me/GIKO_announcement">Telegram Channel</a>

        🔷 Join GIKO <a href="http://t.me/GIKO_discussion">Telegram Group</a>

        🔷 Join OUR <a href="http://t.me/airdropGIKO">Advertiser Channel</a>

        📖 After completing tasks, Write "GIKO TO MOON" in the Group""")
    await update.callback_query.message.reply_html(message_text)
    
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    return ConversationHandler.END

async def SOL_Address_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    global users
    user_id = update.effective_user.id
    user_name = update.effective_user.username
        
    users[user_id].solAddress = message
    users[user_id].airdropBalance = 15000
    message_text = (
        f"""
    🎉 Congratulations, {user_name}! You've Received 15,000 $GIKO (~100$) as Joining Reward.

    👮 Refer your friends to Earn 7,500 $GIKO (~50$) for Each valid Refer.

    📎 Your Refferal Link: https://t.me/GIKOAirdropBot?start=r05732190645
    """)
    
    keyboard = [
            [InlineKeyboardButton("Balance", callback_data='balance')],
            [InlineKeyboardButton("Referral", callback_data='referral'), InlineKeyboardButton("Withdraw", callback_data='withdraw')],
            [InlineKeyboardButton("Back", callback_data='back'), InlineKeyboardButton("Main Menu", callback_data='mainmenu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    print("---user------", users[user_id])
    await update.message.reply_html(message_text, reply_markup=reply_markup)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Handle all messages from customers """
    # Get the message from the update
    message = update.message.text
    user = update.effective_user
    # Print messages to the console
    if (message == "GIKO TO MOON"):
        message_text = """
        🚀 Follow GIKO Coin on <a href="https://twitter.com/GIKOWorld">Twitter</a> 

    📖 Submit your Twitter username with (@)
        """
        await update.message.reply_html(message_text)
    elif message.startswith("@"):
        global users
        user_id = update.effective_user.id
        user_name = update.effective_user.username
            
        users[user_id].twitterName = message
        message_text = """
        💵 Submit your Solana (SOL) wallet address.

    Submit a Valid address
        """
        await update.message.reply_html(message_text)
        return SOL_ADDRESS_STATE
    
async def handle_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    airdropBalance = users[user_id].airdropBalance
    referralBalance = users[user_id].referralBalance
    message_text = (
        f"""😽Your GIKO Airdrop Balances:

    💵 Airdrop Balance: {airdropBalance} $GIKO ({airdropBalance/150}$)
    🧑‍✈️ Refferal Balance: {referralBalance} $GIKO ({referralBalance/150}$ )

    🐱 Get 7500 $GIKO (~50$) for Each valid Refferal.

    🏆 Refferal Link: <a href="https://t.me/GIKOAirdropBot?start=r05732190645">https://t.me/GIKOAirdropBot?start=r05732190645</a>
    """)
    await update.message.reply_html(message_text)

async def handle_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = ("""
        🙀 Welcome to GIKO Refferal Program.

    🧑‍✈️ Get 7500 $GIKO (~50) for each Valid Refferal. Refer your friends to Earn $GIKO.

    💹 Your Refferal Link: <a href = "https://t.me/GIKOAirdropBot?start=r05732190645">https://t.me/GIKOAirdropBot?start=r05732190645</a>

    📌 Refer at least 5 friends to be Eligible for Airdrop.

    🐱 Website: <a href = "GIKO.xyz">GIKO.xyz</a>            
    """)
    await update.message.reply_html(message_text)
    
async def handle_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = """
        🗓️ Distribution will start on 12th May, 2024.

    🙀 Refer at Least 5 friends to be Eligible for Airdrop.
    """
    await update.message.reply_html(message_text)
    
async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await handle_airdropContent(update, context)
    
async def handle_mainmenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await start(update, context)
        
def main():
    """Run the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(handle_airdropContent, pattern='^airdropContent$'),
            CallbackQueryHandler(handle_balance, pattern='^balance$'),
            CallbackQueryHandler(handle_referral, pattern='^referral$'),
            CallbackQueryHandler(handle_withdraw, pattern='^withdraw$'),
            CallbackQueryHandler(handle_back, pattern='^back$'),
            CallbackQueryHandler(handle_mainmenu, pattern='^mainmenu$'),
            MessageHandler(filters.TEXT, message_handler)
        ],
        states={
            SOL_ADDRESS_STATE: [
                MessageHandler(filters.TEXT, SOL_Address_handler)
            ],
            END_STATE: [
                CallbackQueryHandler(end),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
