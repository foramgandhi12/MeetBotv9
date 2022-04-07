from gscripts.meet import meet, close
from gscripts.login import login
import shutil
import pickle
from telegram.ext import Updater
from telegram.ext import CommandHandler, Filters, MessageHandler
from telegram import ChatAction

import chromium_Scripts
from chromium_Scripts import telegram_bot_sendtext, webdriver, options

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")

updater = Updater(token=BOT_TOKEN, use_context=True)
dp = updater.dispatcher


# Feature addition autowrite userid in .env file

def start(update, context):
    user = update.message.from_user
    context.bot.send_chat_action(chat_id=user.id, action=ChatAction.TYPING)
    telegram_bot_sendtext("Hello {}!".format(user.first_name))
    telegram_bot_sendtext("Your UserID is: {} ".format(user.id))
    return 1
    # Removed ChromeDriver Dependency
    # if chromedriverCheck():
    #     from chromium_Scripts import str1

    #     update.message.reply_text(
    #         "please download correct chromedriver version :", str1[0:2]
    #     )
    #     update.message.reply_text(
    #         "Download it from here :", "https://chromedriver.chromium.org/downloads"
    #     )


def echo(update, context):
    update.message.reply_text(
        "This is not a valid command\nUse /help to list out the available commands"
    )


def help(update, context):
    user = update.message.from_user
    if user.id == int(USER_ID):
        telegram_bot_sendtext(
            "/login - Login in Google Meet\n/meet - Join a meet\n/close - Leave the meeting\n/status - Screenshot of "
            "Joined meet\n/restart - restart the GMeetrobot\n/reset - Reset chrome browser\n/owner-To know about "
            "me\n/quit-To quit script\n/help - To Display this message "
        )
        return 1
    else:
        telegram_bot_sendtext("You are not authorized to use this bot.\nUse /owner to know about me")
        # update.message.reply_text(
        #     "You are not authorized to use this bot.\nUse /owner to know about me"
        # )
        return 0


def owner(update, context):
    telegram_bot_sendtext(
        "My code lies around the whole Internet 😇\nIt was assembled, modified and upgraded by Pathak Pratik\nSource "
        "Code is available here👇\nhttps://github.com/zpratikpathak/"
    )
    return 1


# To do, send a message to the user when the bot is restarted : Finished
def restart(update, context):
    user = update.message.from_user
    if user.id == int(USER_ID):
        telegram_bot_sendtext("Restarting, Please wait!")
        r = open("restart.pkl", "wb")
        pickle.dump("restart msg check", r)
        r.close()
        chromium_Scripts.browser.quit()

        if os.path.exists("restart.pkl"):
            try:
                os.remove("restart.pkl")
                telegram_bot_sendtext("Bot Restarted")
            except:
                pass
        chromium_Scripts.browser = webdriver.Chrome(options=options)  # restart the chrome window
        return 1
    else:
        telegram_bot_sendtext("You are not authorized to use this bot.\nUse /owner to know about me")
        return 0


def status(update, context):
    user = update.message.from_user
    if user.id == int(USER_ID):
        chromium_Scripts.browser.save_screenshot("snapshot.png")
        f = open("snapshot.png", "rb")
        context.bot.send_chat_action(
            chat_id=USER_ID, action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(
            chat_id=USER_ID, photo=f, timeout=100
        )
        try:
            os.remove("snapshot.png")
        except:
            f.close()
            os.remove("snapshot.png")
        return 1
    else:
        telegram_bot_sendtext("You are not authorized to use this bot.\nUse /owner to know about me")
        return 0


def reset(update, context):
    user = update.message.from_user
    if user.id == int(USER_ID):
        if os.path.exists("ChromiumData") or os.path.exists("../gmeet.pkl"):

            try:
                chromium_Scripts.browser.quit()
                shutil.rmtree("ChromiumData")
                try:
                    os.remove("../gmeet.pkl")
                except:
                    pass
                telegram_bot_sendtext("Chrome Reset Successful")
                chromium_Scripts.browser = webdriver.Chrome(options=options)  # reset the chrome window
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        else:
            telegram_bot_sendtext("Browser is already clear...")
        return 1
    else:
        telegram_bot_sendtext("You are not authorized to use this bot.\nUse /owner to know about me")
        return 0


def q(update, context):
    print("Trying to quit")

    user = update.message.from_user
    if user.id == int(USER_ID):
        context.bot.send_message(
            chat_id=USER_ID,
            text="The script will now quit",
        )
        chromium_Scripts.browser.quit()
        os._exit(0)
    else:
        update.message.reply_text(
            "You are not authorized to use this bot.\nUse /owner to know about me"
        )


def main():
    dp.add_handler(CommandHandler("start", start, run_async=True))
    dp.add_handler(CommandHandler("help", help, run_async=True))
    dp.add_handler(CommandHandler("owner", owner, run_async=True))
    dp.add_handler(CommandHandler("restart", restart, run_async=True))
    dp.add_handler(CommandHandler("status", status, run_async=True))
    dp.add_handler(CommandHandler("reset", reset, run_async=True))
    dp.add_handler(CommandHandler("login", login, run_async=True))
    dp.add_handler(CommandHandler("meet", meet, run_async=True))
    dp.add_handler(CommandHandler("close", close, run_async=True))
    dp.add_handler(CommandHandler("quit", q, run_async=True))
    dp.add_handler(MessageHandler(Filters.text, echo, run_async=True))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

# To Do: Add restart feature : Finished
