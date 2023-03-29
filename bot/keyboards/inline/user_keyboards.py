from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


feedback_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="😠", callback_data="feedback:bad"),
            InlineKeyboardButton(text="😐", callback_data="feedback:neutral"),
            InlineKeyboardButton(text="😍", callback_data="feedback:good"),
        ],
    ],
    resize_keyboard=True,
)
