import chromium_Scripts
from chromium_Scripts import webdriver, options
from telegram import ChatAction
import os
import time
from dotenv import load_dotenv

load_dotenv()
USER_ID = os.getenv("USER_ID")

def meet_url(context, url_meet):
    # browser.get(url_meet)
    # context.bot.send_message(chat_id=USER_ID, text="Joined the meet")

    try:
        if os.path.exists("../gmeet.pkl"):
            pass
        else:
            context.bot.send_message(
                chat_id=USER_ID,
                text="You're not logged in please run /login command to login. Then try again!",
            )
            return

        chromium_Scripts.browser.get(url_meet)
        time.sleep(3)

        chromium_Scripts.browser.save_screenshot("ss.png")
        context.bot.send_chat_action(
            chat_id=USER_ID, action=ChatAction.UPLOAD_PHOTO)
        mid = context.bot.send_photo(
            chat_id=USER_ID, photo=open("ss.png", "rb"), timeout=120
        ).message_id
        os.remove("ss.png")

        if chromium_Scripts.browser.find_elements_by_xpath(
            '//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div'
        ):
            chromium_Scripts.browser.find_element_by_xpath(
                '//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div'
            ).click()
            time.sleep(3)

        # Due to recent Google Chrome update, a "pop up dialogue" shows up if the user does not have cam/mic permissions
        # This was causing the script to crash because the button to join the meet was being rendered unclickable
        # if the dismiss prompt is found, clicks on the dismiss button, otherwise clicks the join button
        try:
            print("Clicked dismiss")
            chromium_Scripts.browser.find_element_by_xpath("//*[@id='yDmH0d']/div[3]/div[2]/div/div[2]/button").click()
            time.sleep(10)
        except:
            print("Dismiss element not found")
            time.sleep(10)
        try:
            chromium_Scripts.browser.find_element_by_xpath(
                "//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Ask to join')]"
            ).click()
            time.sleep(10)
        except:
            chromium_Scripts.browser.find_element_by_xpath(
                "//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Join now')]"
            ).click()
            time.sleep(10)

        context.bot.send_chat_action(chat_id=USER_ID, action=ChatAction.TYPING)

        time.sleep(10)

        chromium_Scripts.browser.save_screenshot("screenshot.png")
        context.bot.send_chat_action(
            chat_id=USER_ID, action=ChatAction.UPLOAD_PHOTO)
        mid = context.bot.send_photo(
            chat_id=USER_ID, photo=open("screenshot.png", "rb"), timeout=120
        ).message_id
        os.remove("screenshot.png")

        context.bot.send_chat_action(chat_id=USER_ID, action=ChatAction.TYPING)
        time.sleep(3)
        context.bot.send_message(
            chat_id=USER_ID,
            text="Attending your lecture.\nI got your back 😉\nYou can chill :v",
        )

    except Exception as e:
        chromium_Scripts.browser.quit()
        context.bot.send_message(
            chat_id=USER_ID, text="Error occurred! Fix error and retry!"
        )
        context.bot.send_message(
            chat_id=USER_ID, text="Try /reset to fix the issue")
        context.bot.send_message(chat_id=USER_ID, text=str(e))
        chromium_Scripts.browser = webdriver.Chrome(options=options)  # reset the chrome window


def meet(update, context):
    user = update.message.from_user
    if user["id"] == int(USER_ID):
        context.bot.send_chat_action(chat_id=USER_ID, action=ChatAction.TYPING)
        url_meet = update.message.text.split()[-1]
        if len(url_meet) == 12:
            url_meet = "https://meet.google.com/{}".format(url_meet)
            meet_url(context, url_meet)
        elif len(url_meet) == 10:
            url_meet = url_meet[:3] + "-" + url_meet[3:5] + "-" + url_meet[5:]
            url_meet = "https://meet.google.com/{}".format(url_meet)
            meet_url(context, url_meet)
        elif len(url_meet) > 5:
            meet_url(context, url_meet)
        else:
            context.bot.send_message(
                chat_id=USER_ID,
                text="Oops! You forget to pass the correct google meet url",
            )
            context.bot.send_message(
                chat_id=USER_ID, text="Use /meet command like this 👇"
            )
            context.bot.send_message(
                chat_id=USER_ID, text="/meet https://meet.google.com/meet-code-value"
            )
    else:
        update.message.reply_text(
            "You are not authorized to use this bot.\nUse /owner to know about me"
        )


def close(update, context):
    user = update.message.from_user
    if user["id"] == int(USER_ID):
        context.bot.send_chat_action(chat_id=USER_ID, action=ChatAction.TYPING)
        # Click the leave call button if the object is found
        try:
            chromium_Scripts.browser.find_element_by_xpath(
                '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[2]/div/div[7]/span/button'
            ).click()
            time.sleep(3)
            # click the just leave the call button if button is there
            try:
                chromium_Scripts.browser.find_element_by_xpath(
                    '//*[@id="yDmH0d"]/div[3]/div[2]/div/div[2]/button[1]'
                ).click()
                time.sleep(3)
            except:
                pass

            chromium_Scripts.browser.save_screenshot("screenshot.png")
            context.bot.send_chat_action(
                chat_id=USER_ID, action=ChatAction.UPLOAD_PHOTO)
            mid = context.bot.send_photo(
                chat_id=USER_ID, photo=open("screenshot.png", "rb"), timeout=120
            ).message_id
            os.remove("screenshot.png")

            context.bot.send_message(
                chat_id=USER_ID,
                text="Bye! Hope you had a great meeting!\nSee you soon! 😉",
            )
        except:
            context.bot.send_message(
                chat_id=USER_ID,
                text="You are not in a meeting!",
            )
    else:
        update.message.reply_text(
            "You are not authorized to use this bot.\nUse /owner to know about me"
        )
