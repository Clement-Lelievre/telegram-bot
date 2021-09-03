from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,  ParseMode
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackContext
import re, os
from dotenv import load_dotenv
import logging
from utils import *
from messages import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# using the token provided at creation by the Botfather
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Our states, as integers
WELCOME, QUESTION , CANCEL , CORRECT = range(4)

# The entry function
def start(update_obj: Update, context: CallbackContext):
    """The action that happens at inception (command /start)"""
    # send the question, and show the keyboard markup (suggested answers)
    first_name = update_obj.effective_user.first_name
    update_obj.message.reply_text(START_MSG.format(first_name),
        reply_markup= ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True),
        parse_mode=ParseMode.HTML
    )
    # go to the WELCOME state
    return WELCOME

# in the WELCOME state, check if the user wants to answer a question
def welcome(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        # send question, and go to the QUESTION state
        randomize_numbers(update_obj, context)
        return QUESTION
    else:
        # go to the CANCEL state
        return CANCEL

# in the QUESTION state
def question(update_obj, context):
    # expected solution
    solution = int(context.user_data['rand_x']) + int(context.user_data['rand_y'])
    # check if the solution was correct
    if solution == int(update_obj.message.text):
        # correct answer, ask the user if he found tutorial helpful, and go to the CORRECT state
        first_name = update_obj.effective_user.first_name
        update_obj.message.reply_text(CONGRATS.format(first_name))
        return CORRECT
    else:
        # wrong answer, reply, send a new question, and loop on the QUESTION state
        update_obj.message.reply_text("Wrong answer :'(")
        # send another random numbers calculation
        randomize_numbers(update_obj, context)
        return QUESTION

# in the CORRECT state
def correct(update_obj: Update, context: CallbackContext):
    if update_obj.message.text.lower() in ['yes', 'y']:
        update_obj.message.reply_text("Glad it was useful! ^^")
    else:
        update_obj.message.reply_text("You must be a programming wizard already!")
    # get the user's first name
    #first_name = update_obj.message.from_user['first_name']
    first_name = update_obj.effective_user.first_name
    update_obj.message.reply_text(BYE.format(first_name))
    return ConversationHandler.END

def cancel(update_obj: Update, context: CallbackContext):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}!", reply_markup= ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# a regular expression that matches yes or no
yes_no_regex = re.compile(r'^(yes|no|y|n)$', re.IGNORECASE)

def main() -> None:
    """Run the bot."""
    # Create an updater object with our API Key
    updater = Updater(API_KEY)
    # Retrieve the dispatcher, which will be used to add handlers
    dispatcher = updater.dispatcher
    # Create our ConversationHandler
    handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), MessageHandler(Filters.regex('^(I wanna play|a game please)$'), start)],
        states={
                WELCOME: [MessageHandler(Filters.regex(yes_no_regex), welcome)],
                QUESTION: [MessageHandler(Filters.regex(r'^\d+$'), question)],
                CANCEL: [MessageHandler(Filters.regex(yes_no_regex), cancel)],
                CORRECT: [MessageHandler(Filters.regex(yes_no_regex), correct)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
        conversation_timeout=15.0
        )

    # add the handler to the dispatcher
    dispatcher.add_handler(handler)
    # start polling for updates from Telegram
    updater.start_polling()
    # block until a signal (like one sent by CTRL+C) is sent
    updater.idle()

if __name__ == '__main__':
    main()
