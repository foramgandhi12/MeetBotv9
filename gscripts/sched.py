from chromium_Scripts import browser
from telegram import ChatAction
import os
import time
import datetime
import schedule
import time
from dotenv import load_dotenv
import automate
from gscripts.meet import meet, meet_url

load_dotenv()
USER_ID = os.getenv("USER_ID")

userSched = {
    "sunday": [],
    "monday": [],
    "tuesday": [],
    "wednesday": [],
    "thursday": [],
    "friday": [],
    "saturday": []
}

week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

today = automate.today


def sched(update, context):
    user = update.message.from_user
    if user["id"] == int(USER_ID):
        context.bot.send_chat_action(chat_id=USER_ID, action=ChatAction.TYPING)
        info = update.message.text.split()  # Array containing all user entered arguments

        dayVal = False
        timeVal = False
        urlVal = False

        if (len(info) != 4):
            context.bot.send_message(
                chat_id=USER_ID,
                text="Make sure you Enter ALL the required arguments. No less and no more."
            )
            context.bot.send_message(
                chat_id=USER_ID,
                text="Use /addws command like this 👇"
            )
            context.bot.send_message(
                chat_id=USER_ID,
                text="/addws <day of the week> <time in 24 hr format without colon> <meet link>"
            )
            context.bot.send_message(
                chat_id=USER_ID,
                text="Example: /addws monday 1340 https://meet.google.com/meet-code"
            )
        else:
            day = info[1]
            meetTime = info[2]
            url_meet = info[-1]

            # Validate Meet Link
            if len(url_meet) == 12:
                url_meet = "https://meet.google.com/{}".format(url_meet)
                urlVal = True
            elif len(url_meet) == 10:
                url_meet = url_meet[:3] + "-" + url_meet[3:5] + "-" + url_meet[5:]
                url_meet = "https://meet.google.com/{}".format(url_meet)
                urlVal = True
            elif len(url_meet) > 5 and len(url_meet) <= 36:
                urlVal = True
            else:
                context.bot.send_message(
                    chat_id=USER_ID,
                    text="Oops! You forget to pass the correct google meet url",
                )
                context.bot.send_message(
                    chat_id=USER_ID, text="send meet link like this 👇"
                )
                context.bot.send_message(
                    chat_id=USER_ID, text="https://meet.google.com/meet-code-value"
                )

                urlVal = False

            # Validate Day
            if (day.lower() not in week):
                context.bot.send_message(
                    chat_id=USER_ID,
                    text="You entered an invalid day of the week. Enter one of the following days:"
                )
                context.bot.send_message(
                    chat_id=USER_ID,
                    text="Sunday Monday Tuesday Wednesday Thursday Friday Saturday"
                )
                dayVal = False
            else:
                dayVal = True
                day = day.lower()

            # Validate Time
            if int(meetTime) < 0 or int(meetTime) > 2359 or len(meetTime) < 4:
                context.bot.send_message(
                    chat_id=USER_ID,
                    text="You entered an invalid time. Enter the time in 24 hr format - 4 digits without spaces or "
                         "colon: "
                )
                context.bot.send_message(
                    chat_id=USER_ID,
                    text="Example:\n0000 (refers to 12:00 AM)\n1350 (refers to 1:50 PM)"
                )

                timeVal = False
            else:
                timeVal = True

            if (dayVal and timeVal and urlVal):
                print(day + " " + meetTime + " " + url_meet)

                userSched[day].append(meetTime + " " + url_meet)

                context.bot.send_message(
                    chat_id=USER_ID,
                    text="Successfully added to schedule!"
                )

                print(userSched)

                print(automate.today)

    else:
        update.message.reply_text(
            "You are not authorized to use this bot.\nUse /owner to know about me"
        )


def checkTime(*args):
    print("checking")

    con = args[0]
    global temp
    global meetlink
    meetlink = ""
    currTime = datetime.datetime.now().strftime("%H%M")

    meetsInDay = len(userSched[today])

    for info in userSched[today]:
        if currTime in info:
            meetlink = info.split()[-1]
            meet_url(con, meetlink)
            break


def checkSched(update, context):
    schedule.every(1).minutes.do(checkTime, context)

    while 1:
        schedule.run_pending()

        time.sleep(3)

