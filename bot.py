import json
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def load_jokes():
    with open('jokes.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_jokes(jokes):
    with open('jokes.json', 'w', encoding='utf-8') as file:
        json.dump(jokes, file, ensure_ascii=False, indent=2)

JOKES = load_jokes()

CATEGORIES = {
    'Happy': 'Happy',
    'Sad': 'Sad',
    'Scary': 'Scary',
    'Angry': 'Angry',
    'Mysterious': 'Mysterious'
}

def get_random_joke_weighted(category: str):
    jokes_list = JOKES.get(category, [])
    weights = [joke.get('rating', 0) + 1 for joke in jokes_list]
    index = random.choices(range(len(jokes_list)), weights=weights, k=1)[0]
    return jokes_list[index], index

def update_rating(category: str, joke_index: int, is_like: bool):
    if category not in JOKES:
        return False
    
    if joke_index < 0 or joke_index >= len(JOKES[category]):
        return False
    
    joke = JOKES[category][joke_index]
    current_rating = joke.get('rating', 0)
    current_votes = joke.get('votes', 0)
    
    if is_like:
        new_rating = current_rating + 1
    else:
        new_rating = current_rating - 1
    
    joke['rating'] = new_rating
    joke['votes'] = current_votes + 1
    
    save_jokes(JOKES)
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text, callback_data=cat)]
        for cat, text in CATEGORIES.items()
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "+ - — rate jokes so the worst will be later replaced",
        reply_markup=reply_markup
    )

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton(text, callback_data=cat)]
        for cat, text in CATEGORIES.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "Choose your mood:",
        reply_markup=reply_markup
    )
    await query.answer()

async def send_joke(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    joke, joke_index = get_random_joke_weighted(category)
    
    joke_text = joke['text']
    rating = joke.get('rating', 0)
    votes = joke.get('votes', 0)
    rating_text = f"⭐ {rating}" if votes > 0 else "No ratings yet"

    context.user_data['current_joke'] = {
        'category': category,
        'index': joke_index
    }
    
    keyboard = [
        [
            InlineKeyboardButton(f"👍", callback_data=f"like"),
            InlineKeyboardButton(f"👎", callback_data=f"dislike")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    full_text = f"{joke_text}\n\n{rating_text}"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            full_text,
            reply_markup=reply_markup
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            full_text,
            reply_markup=reply_markup
        )

async def rate_and_return(update: Update, context: ContextTypes.DEFAULT_TYPE, is_like: bool):
    query = update.callback_query
    joke_data = context.user_data.get('current_joke')
    
    if joke_data:
        category = joke_data['category']
        joke_index = joke_data['index']
        
        success = update_rating(category, joke_index, is_like)
        
        if success:
            await query.answer(f"{'👍' if is_like else '👎'} Thanks for rating!")
        else:
            await query.answer("Error", show_alert=True)
    
    keyboard = [
        [InlineKeyboardButton(text, callback_data=cat)]
        for cat, text in CATEGORIES.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "Сhoose your mood:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "like":
        await rate_and_return(update, context, is_like=True)
        
    elif data == "dislike":
        await rate_and_return(update, context, is_like=False)
        
    elif data in CATEGORIES:
        await send_joke(update, context, data)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /help"""
    await update.message.reply_text(
        "*How to use:*\n\n"
        "• Press `/start` — see mood buttons\n"
        "• Choose a mood — get a joke\n"
        "• Rate the joke 👍 👎 — you'll automatically return to the menu\n"
        "• Choose another mood for more jokes\n\n"
        "Commands:\n"
        "`/Happy` — Funny joke\n"
        "`/Sad` — Sad humor\n"
        "`/Scary` — Scary joke\n"
        "`/Angry` — Angry joke\n"
        "`/Mysterious` — Mysterious joke",
        parse_mode='Markdown'
    )

async def category_command(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    await send_joke(update, context, category)

async def Happy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_command(update, context, 'Happy')

async def Sad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_command(update, context, 'Sad')

async def Scary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_command(update, context, 'Sacry')

async def Angry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_command(update, context, 'Angry')

async def Mysterious(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_command(update, context, 'Mysterious')

def main():
    TOKEN = "8271299367:AAHUlaWXR5a21rTYlgS3Z9rYWsDEqsR_Q4Q"
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("Happy", Happy))
    app.add_handler(CommandHandler("Sad", Sad))
    app.add_handler(CommandHandler("Scary", Scary))
    app.add_handler(CommandHandler("Angry", Angry))
    app.add_handler(CommandHandler("Mysterious", Mysterious))

    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()