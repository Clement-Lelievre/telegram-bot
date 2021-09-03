from random import randint
from telegram import Update
from telegram.ext import CallbackContext


def randomize_numbers(update_obj: Update, context: CallbackContext):
    """a helper function that generates new numbers and sends the question"""
    # store the numbers in the context
    context.user_data['rand_x'], context.user_data['rand_y'] = randint(1,1000), randint(1,1000)
    # send the question
    update_obj.message.reply_text(f"Calculate {context.user_data['rand_x']} + {context.user_data['rand_y']}")
    
def help(update_obj: Update, context: CallbackContext):
    update_obj.message.reply_text("""This bot lets you play a calculation game. To launch the game, you can either use /start, 
    or type one of the following: I wanna play,a game please, game!""")
