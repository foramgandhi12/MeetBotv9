import datetime
import os
import time

import automate
import schedule
from chromium_Scripts import telegram_bot_sendtext
from dotenv import load_dotenv
from gscripts.meet import meet_url
from telegram import ChatAction

load_dotenv()
USER_ID = os.getenv("USER_ID")

# initialize empty dictionary of weekdays
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

# get today's date and time
try:
    today = automate.today
except:
    pass


# adds user's meeting date and time to their schedule
def sched(update, context):
    user = update.message.from_user
    
    # authorized user access
    if user.id == int(USER_ID):
        context.bot.send_chat_action(chat_id=USER_ID, action=ChatAction.TYPING) # bot is typing
        info = update.message.text.split()  # Array containing all user entered arguments

        dayVal = False
        timeVal = False
        urlVal = False

        # input validation
        
        # validate number of arguments
        if len(info) != 4:
            telegram_bot_sendtext("Make sure you Enter ALL the required arguments. No less and no more.")
            telegram_bot_sendtext("Use /addws command like this 👇")
            telegram_bot_sendtext("/addws <day of the week> <time in 24 hr format without colon> <meet link>")
            telegram_bot_sendtext("Example: /addws monday 1340 https://meet.google.com/meet-code")
            return 0
        else:
            day = info[1]
            meetTime = info[2]
            url_meet = info[-1]

            # validate meet link
            if len(url_meet) == 12:
                url_meet = "https://meet.google.com/{}".format(url_meet)
                urlVal = True
            elif len(url_meet) == 10:
                url_meet = url_meet[:3] + "-" + url_meet[3:5] + "-" + url_meet[5:]
                url_meet = "https://meet.google.com/{}".format(url_meet)
                urlVal = True
            elif 5 < len(url_meet) <= 36:
                urlVal = True
            else:
                telegram_bot_sendtext("Oops! You forget to pass the correct google meet url")
                telegram_bot_sendtext("send meet link like this 👇")
                telegram_bot_sendtext("https://meet.google.com/meet-code-value")
                urlVal = False
                return 2

            # validate day
            if day.lower() not in week: # day must exist within week array
                telegram_bot_sendtext("You entered an invalid day of the week. Enter one of the following days:")
                telegram_bot_sendtext("Sunday Monday Tuesday Wednesday Thursday Friday Saturday")
                dayVal = False
            else:
                dayVal = True
                day = day.lower()

            # validate time
            if int(meetTime) < 0 or int(meetTime) > 2359 or len(meetTime) < 4:
                telegram_bot_sendtext("You entered an invalid time. Enter the time in 24 hr format - 4 digits without "
                                      "spaces or colon: ")
                telegram_bot_sendtext("Example:\n0000 (refers to 12:00 AM)\n1350 (refers to 1:50 PM)")

                timeVal = False
                return 3
            else:
                timeVal = True

            if dayVal and timeVal and urlVal:
                print(day + " " + meetTime + " " + url_meet)

                # add meeting to schedule
                userSched[day].append(meetTime + " " + url_meet)
                telegram_bot_sendtext("Successfully added to schedule!")

                print(userSched)

                print(automate.today)
                return 1
            
    # unauthorized user access
    else:
        telegram_bot_sendtext("You are not authorized to use this bot.\nUse /owner to know about me")
        return -1


# check the current time
def checkTime(*args):
    print("checking")

    con = args[0]
    global temp
    global meetlink
    meetlink = ""
    currTime = datetime.datetime.now().strftime("%H%M")

    # if a meeting is scheduled for today, then join
    for info in userSched[today]:
        if currTime in info:
            meetlink = info.split()[-1]
            meet_url(con, meetlink)
            return 1
    return 0


# check the time every minute when /ssch command is invoked
def checkSched(update, context):
    schedule.every(1).minutes.do(checkTime, context)

    while 1:
        schedule.run_pending()
        time.sleep(3)

