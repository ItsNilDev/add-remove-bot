
import telebot
import datetime
import re

date = datetime.datetime.now()
bot = telebot.TeleBot("TOKEN", parse_mode=None)

# Enter Admins
admins_username = ["Omidan2016", "ItzSyntax_Error"]

# Start/Help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Enter A Username to add to this group and delete them after 30 days: ")

# Update to see if anyone should be kicked or not
@bot.message_handler(commands=['update'])
def update_members(message):
    try:
        # Open the database
        with open("database.txt", "wr") as database:
            # Find who should be kicked
            should_be_kicked = []
            date_now = date.strftime("%Y-%m-%d")
            for line in database:
                # goddam regex :woozy_face:
                x = re.search(": ([\S]*)$", line)
                if(x.group(1).strip()):
                    d1 = datetime.datetime.strptime(x.group(1).strip(), "%Y-%m-%d")
                    d2 = datetime.datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d")
                    if(abs((d1-d2).days) >= 30):
                        user = re.search("@([\S]*)$", line)
                        should_be_kicked.append(("This user should be kicked: {0}".format(user.group(0))))
            bot.reply_to(message, should_be_kicked)
    except FileNotFoundError:
        bot.reply_to(message, "The Database file doesn't exist, Please add some members!")


# Adding a User to the group/channel and delete them after a certain amount of time
@bot.message_handler(regexp="@([\S]*)$")
def echo_all(message):
    # Checking if the user is admin or not
    if(message.from_user.username in admins_username):
        bot.reply_to(message, "Added the user: {0} to my database!".format(message.text))
        # TODO: Implement adding user to the database/file
        # Saving a user to the database and check if they should be removed
        with open("database.txt", 'wr') as database:
            database.write("{0}: {1} \n".format(message.text, date.strftime("%Y-%m-%d")))
    else:
        bot.reply_to(message, "You can not do this because you're not admin.")



# Bot Handling
bot.polling()
