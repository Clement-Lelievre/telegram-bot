from random import randint

# helper function, generates new numbers and sends the question
def randomize_numbers(update_obj, context):
    # store the numbers in the context
    context.user_data['rand_x'], context.user_data['rand_y'] = randint(1,1000), randint(1,1000)
    # send the question
    update_obj.message.reply_text(f"Calculate {context.user_data['rand_x']} + {context.user_data['rand_y']}")