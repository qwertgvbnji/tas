import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load configuration
from config import BOT_TOKEN, ADMIN_ID

# Dictionary to store user choices
user_choices = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Dice Game! Use /roll to start a game.')

def roll(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    if chat_id in user_choices:
        update.message.reply_text('A game is already in progress in this chat.')
        return

    user_choices[chat_id] = {}
    update.message.reply_text('A new game has started! Each player should choose a number between 1 and 6.')

def guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    text = update.message.text

    if chat_id not in user_choices:
        update.message.reply_text('No game is in progress. Use /roll to start a new game.')
        return

    try:
        guess_number = int(text)
        if guess_number < 1 or guess_number > 6:
            update.message.reply_text('Please choose a number between 1 and 6.')
            return

        user_choices[chat_id][user_id] = guess_number

        if len(user_choices[chat_id]) == 2:
            dice_roll = random.randint(1, 6)
            update.message.reply_text(f'The dice rolled: {dice_roll}')

            winners = []
            for uid, guess in user_choices[chat_id].items():
                if guess == dice_roll:
                    winners.append(uid)

            if winners:
                winner_names = [f'User {uid}' for uid in winners]
                update.message.reply_text(f'Congratulations {", ".join(winner_names)}! You guessed correctly!')
            else:
                update.message.reply_text('No one guessed correctly. Better luck next time!')

            del user_choices[chat_id]
        else:
            update.message.reply_text('Waiting for the other player to choose a number.')
    except ValueError:
        update.message.reply_text('Please enter a valid number between 1 and 6.')

def main() -> None:
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("roll", roll))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, guess))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
