from telegram.ext import Updater
from telegram.ext import CommandHandler, Job, Filters, MessageHandler
from telegram import ChatAction

from chromium_Scripts import browser, chromedriverCheck, telegram_bot_sendtext

from os import execl
from sys import executable

import os
from dotenv import load_dotenv

load_dotenv()

import pickle

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")

updater = Updater(token=BOT_TOKEN, use_context=True)
dp = updater.dispatcher

# Feature addition autowrite userid in .env file
def start(update, context):
    user = update.message.from_user
    # print(user)
    context.bot.send_chat_action(chat_id=user["id"], action=ChatAction.TYPING)
    update.message.reply_text("Hello {}!".format(user["first_name"]))
    update.message.reply_text("Your UserID is: {} ".format(user["id"]))

    if chromedriverCheck():
        from chromium_Scripts import str1

        update.message.reply_text(
            "please download correct chromedriver version :", str1[0:2]
        )
        update.message.reply_text(
            "Download it from here :", "https://chromedriver.chromium.org/downloads"
        )


def echo(update, context):
    update.message.reply_text(
        "This is not a valid command\nUse /help to list out the available commands"
    )


def help(update, context):
    user = update.message.from_user
    if user["id"] == int(USER_ID):
        context.bot.send_message(
            chat_id=USER_ID,
            text="/mlogin - To login your account\n/meet - To join a meet (Use Example: '/meet https://meet.google.com/mee-tco-deval')\n/status - To get current Screenshot of Joined meet\n/exit - To leave a meeting\n/reset - To reset chromium browser (in Development)\n/owner-To know about me\n/help - To Display this message",
        )
    else:
        update.message.reply_text(
            "You are not authorized to use this bot.\nUse /owner to know about me"
        )


def owner(update, context):
    update.message.reply_text(
        "My code lies around the whole Internet 😇\nIt was assembled, modified and upgraded by Pathak Pratik\nSource Code is available here👇\nhttps://github.com/zpratikpathak/",
    )


# To do, send a message to the user when the bot is restarted
def restart(update, context):
    user = update.message.from_user
    if user["id"] == int(USER_ID):
        context.bot.send_message(chat_id=USER_ID, text="Restarting, Please wait!")
        pickle.dump("restart msg check", open("restart.pkl", "wb"))
        browser.quit()
        execl(executable, executable, "automate.py")
    else:
        update.message.reply_text(
            "You are not authorized to use this bot.\nUse /owner to know about me"
        )


def main():

    if os.path.exists("restart.pkl"):
        try:
            os.remove("restart.pkl")
            telegram_bot_sendtext("Bot Restarted")
        except:
            pass

    dp.add_handler(CommandHandler("start", start, run_async=True))
    dp.add_handler(CommandHandler("help", help, run_async=True))
    dp.add_handler(CommandHandler("owner", owner, run_async=True))
    dp.add_handler(CommandHandler("restart", restart, run_async=True))

    dp.add_handler(MessageHandler(Filters.text, echo, run_async=True))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

# To Do: Add restart feature
