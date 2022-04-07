import chromium_Scripts
from telegram import ChatAction
import os
import pickle
import time
from chromium_Scripts import telegram_bot_sendtext

from dotenv import load_dotenv

load_dotenv()
USER_ID = os.getenv("USER_ID")
GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")


def login(update, context):
    user = update.message.from_user
    if user.id == int(USER_ID):
        if os.path.exists("../gmeet.pkl"):
            telegram_bot_sendtext("Already Logged In! Run /meet meeting url to join meeting")
            telegram_bot_sendtext("Still getting some error? try using /reset")
            return 0
        try:
            '''
            context.bot.send_chat_action(chat_id=user["id"], action=ChatAction.TYPING)
            update.message.reply_text("Logging in...")
            browser.get(
                "https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Afad07e7074c3d678%2C10%3A1601127482%2C16%3A9619c3b16b4c5287%2Ca234368b2cab7ca310430ff80f5dd20b5a6a99a5b85681ce91ca34820cea05c6%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22d18871cbc2a3450c8c4114690c129bde%22%7D&response_type=code&flowName=GeneralOAuthFlow"
            )
            time.sleep(2)
            browser.find_element_by_id("identifierId").send_keys(GMAIL_USERNAME)
            time.sleep(7)
            browser.find_element_by_id("identifierNext").click()
            time.sleep(2)
            browser.find_element_by_name("password").send_keys(GMAIL_PASSWORD)
            time.sleep(7)
            browser.find_element_by_id("passwordNext").click()
            time.sleep(2)
            update.message.reply_text("Logged in!")
            browser.get("https://meet.google.com/")
            browser.save_screenshot("snapshot.png")
            context.bot.send_chat_action(
                chat_id=USER_ID, action=ChatAction.UPLOAD_PHOTO
            )
            context.bot.send_photo(
                chat_id=USER_ID, photo=open("snapshot.png", "rb"), timeout=100
            )

            os.remove("snapshot.png")
            '''
            update.message.reply_text("Logging in...")
            context.bot.send_chat_action(
                chat_id=user.id, action=ChatAction.TYPING)
            chromium_Scripts.browser.get(
                "https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Afad07e7074c3d678%2C10%3A1601127482%2C16%3A9619c3b16b4c5287%2Ca234368b2cab7ca310430ff80f5dd20b5a6a99a5b85681ce91ca34820cea05c6%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22d18871cbc2a3450c8c4114690c129bde%22%7D&response_type=code&flowName=GeneralOAuthFlow"
            )
            username = chromium_Scripts.browser.find_element_by_id("identifierId")
            username.send_keys(GMAIL_USERNAME)
            nextButton = chromium_Scripts.browser.find_element_by_id("identifierNext")
            nextButton.click()
            time.sleep(7)

            chromium_Scripts.browser.save_screenshot("ss.png")
            try:
                context.bot.send_chat_action(
                    chat_id=USER_ID, action=ChatAction.UPLOAD_PHOTO)
                mid = context.bot.send_photo(
                    chat_id=USER_ID, photo=open("ss.png", "rb"), timeout=120
                ).message_id
                os.remove("ss.png")
            except:
                pass

            password = chromium_Scripts.browser.find_element_by_xpath(
                "//input[@class='whsOnd zHQkBf']")
            password.send_keys(GMAIL_PASSWORD)
            signInButton = chromium_Scripts.browser.find_element_by_id("passwordNext")
            signInButton.click()
            time.sleep(7)

            if chromium_Scripts.browser.find_elements_by_xpath('//*[@id="authzenNext"]/div/button/div[2]'):
                context.bot.send_chat_action(
                    chat_id=USER_ID, action=ChatAction.TYPING)
                telegram_bot_sendtext("Need Verification. Please Verify")
                chromium_Scripts.browser.find_element_by_xpath(
                    '//*[@id="authzenNext"]/div/button/div[2]'
                ).click()
                time.sleep(5)

                chromium_Scripts.browser.save_screenshot("ss.png")
                try:
                    context.bot.send_chat_action(
                        chat_id=USER_ID, action=ChatAction.UPLOAD_PHOTO)
                    mid = context.bot.send_photo(
                        chat_id=USER_ID, photo=open("ss.png", "rb"), timeout=120
                    ).message_id
                    os.remove("ss.png")
                except:
                    pass
                time.sleep(20)

            chromium_Scripts.browser.get("https://meet.google.com")
            chromium_Scripts.browser.save_screenshot("ss.png")
            try:
                context.bot.send_chat_action(
                    chat_id=USER_ID, action=ChatAction.UPLOAD_PHOTO)
                mid = context.bot.send_photo(
                    chat_id=USER_ID, photo=open("ss.png", "rb"), timeout=120
                ).message_id
                os.remove("ss.png")
            except:
                pass
            time.sleep(7)
            telegram_bot_sendtext("Logged In Successfully.")
            pickle.dump("Meet Login: True", open("../gmeet.pkl", "wb"))
            return 1
        except:
            telegram_bot_sendtext("Auto login failed!")
            # update.message.reply_text("Auto login failed!")
            chromium_Scripts.browser.get(
                "https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmeet.google.com%2F&service=cl&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
            )
            telegram_bot_sendtext("We have opened login page for you")
            telegram_bot_sendtext("Please login manually")
            telegram_bot_sendtext("Don't worry, it's a one time procedure")

            c = 0
            while True:
                try:
                    if chromium_Scripts.browser.find_elements_by_xpath('//*[@id="gb"]/'):
                        pickle.dump("Meet Login: True",
                                    open("../gmeet.pkl", "wb"))
                        telegram_bot_sendtext("Login Successful")
                        break
                except:
                    pass
                time.sleep(1)
                c += 1
                if c == 300:
                    telegram_bot_sendtext("Login Failed")
                    break

    else:
        telegram_bot_sendtext("You are not authorized to use this bot.\nUse /owner to know about me")
        return -1
    # context.bot.send_chat_action(chat_id=USER_ID, action=ChatAction.TYPING)
