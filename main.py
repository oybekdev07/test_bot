# import json
# import random
# import asyncio
# import logging
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.dispatcher.filters import Command
#
#
# logging.basicConfig(level=logging.INFO)
#
# API_TOKEN = "7917728161:AAGrWOcdJG65W-PwBwwfNl4COu3w1furDlY"  # O'zingizning tokeningizni yozing
#
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()
#
# # JSON fayldan testlarni yuklash
# with open("json.file", "r", encoding="utf-8") as f:
#     ALL_QUESTIONS = json.load(f)
#
# new_keys = ["A", "B", "C", "D"]
#
# for item in ALL_QUESTIONS:
#     if "javoblar" in item and "togri_javob" in item:
#         old_answers = item["javoblar"]
#         correct_key = item["togri_javob"]
#         correct_value = old_answers.get(correct_key)
#         if correct_value is None:
#             raise ValueError(f"Tog‘ri javob yo‘q: {item.get('savol', 'Noma’lum')}")
#         other_items = [(k, v) for k, v in old_answers.items() if k != correct_key]
#         other_items_sample = random.sample(other_items, min(3, len(other_items)))
#         new_items = other_items_sample + [(correct_key, correct_value)]
#         random.shuffle(new_items)
#
#         new_answers = {}
#         new_correct_key = None
#         for i, (old_key, old_value) in enumerate(new_items):
#             new_key = new_keys[i]
#             new_answers[new_key] = old_value
#             if old_key == correct_key:
#                 new_correct_key = new_key
#
#         item["javoblar"] = new_answers
#         item["togri_javob"] = new_correct_key
#
# USER_STATE = {}  # user_id -> {index, score, wrong, section}
#
# SECTION_SIZE = 30
# TOTAL_QUESTIONS = len(ALL_QUESTIONS)
# TOTAL_SECTIONS = (TOTAL_QUESTIONS + SECTION_SIZE - 1) // SECTION_SIZE
#
# def get_question_markup(question):
#     buttons = []
#     for key, val in question["javoblar"].items():
#         buttons.append([InlineKeyboardButton(text=f"{key}) {val}", callback_data=key)])
#     return InlineKeyboardMarkup(inline_keyboard=buttons)
#
# @dp.message(Command("start"))
# async def start_test(message: types.Message):
#     user_id = message.from_user.id
#     USER_STATE[user_id] = {
#         "index": 0,
#         "score": 0,
#         "wrong": 0,
#         "section": 0,
#         "paused": False
#     }
#     await send_next_question(message.chat.id, user_id)
#
# @dp.message(Command("pause"))
# async def pause_test(message: types.Message):
#     user_id = message.from_user.id
#     if user_id in USER_STATE:
#         USER_STATE[user_id]["paused"] = True
#         await message.answer("⏸ Test to‘xtatildi.")
#     else:
#         await message.answer("Siz testni hali boshlamadingiz.")
#
# @dp.message(Command("resume"))
# async def resume_test(message: types.Message):
#     user_id = message.from_user.id
#     if user_id in USER_STATE:
#         USER_STATE[user_id]["paused"] = False
#         await message.answer("▶ Test davom ettirilmoqda.")
#         await send_next_question(message.chat.id, user_id)
#     else:
#         await message.answer("Siz testni hali boshlamadingiz.")
#
# async def send_next_question(chat_id, user_id):
#     user_data = USER_STATE.get(user_id)
#     if not user_data:
#         return
#     idx = user_data["index"]
#
#     question = ALL_QUESTIONS[idx]
#     markup = get_question_markup(question)
#     await bot.send_message(chat_id, f"🧪 Savol {idx + 1}:\n\n{question['savol']}", reply_markup=markup)
#
#     seconds = 0
#     while seconds < 30:
#         if user_data["paused"]:
#             await asyncio.sleep(1)
#             continue
#         await asyncio.sleep(1)
#         seconds += 1
#
#     # vaqt tugadi
#     # agar foydalanuvchi javob bermagan bo‘lsa
#     # index ni oshirib keyingi savolga o‘tamiz
#     user_data = USER_STATE.get(user_id)  # qayta o‘qish, chunki o‘zgargan bo‘lishi mumkin
#     if user_data and user_data["index"] == idx and not user_data["paused"]:
#         user_data["index"] += 1
#         user_data["wrong"] += 1
#         await send_next_question(chat_id, user_id)
#
# @dp.callback_query()
# async def handle_answer(callback: types.CallbackQuery):
#     if callback.data not in ["A", "B", "C", "D"]:
#         await callback.answer()
#         return
#
#     user_id = callback.from_user.id
#     user_data = USER_STATE.get(user_id)
#
#     if not user_data:
#         await callback.message.answer("Iltimos, /start buyrug‘idan boshlang.")
#         await callback.answer()
#         return
#
#     idx = user_data["index"]
#     section = user_data["section"]
#     start_idx = section * SECTION_SIZE
#
#     question = ALL_QUESTIONS[start_idx + idx]
#
#     if callback.data == question["togri_javob"]:
#         await callback.message.answer("✅ To‘g‘ri javob!")
#         user_data["score"] += 1
#     else:
#         togri = question["togri_javob"]
#         await callback.message.answer(f"❌ Noto‘g‘ri. To‘g‘ri javob: {togri}) {question['javoblar'][togri]}")
#         user_data["wrong"] += 1
#
#     user_data["index"] += 1
#     await send_next_question(callback.message.chat.id, user_id)
#     await callback.answer()
#
# if __name__ == "__main__":
#     asyncio.run(dp.start_polling(bot))


import json
import random
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)

API_TOKEN = "7917728161:AAGrWOcdJG65W-PwBwwfNl4COu3w1furDlY"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

with open("json.file", "r", encoding="utf-8") as f:
    ALL_QUESTIONS = json.load(f)

new_keys = ["A", "B", "C", "D"]

for item in ALL_QUESTIONS:
    if "javoblar" in item and "togri_javob" in item:
        old_answers = item["javoblar"]
        correct_key = item["togri_javob"]
        correct_value = old_answers.get(correct_key)
        if correct_value is None:
            raise ValueError(f"Tog‘ri javob yo‘q: {item.get('savol', 'Noma’lum')}")
        other_items = [(k, v) for k, v in old_answers.items() if k != correct_key]
        other_items_sample = random.sample(other_items, min(3, len(other_items)))
        new_items = other_items_sample + [(correct_key, correct_value)]
        random.shuffle(new_items)

        new_answers = {}
        new_correct_key = None
        for i, (old_key, old_value) in enumerate(new_items):
            new_key = new_keys[i]
            new_answers[new_key] = old_value
            if old_key == correct_key:
                new_correct_key = new_key

        item["javoblar"] = new_answers
        item["togri_javob"] = new_correct_key

USER_STATE = {}

SECTION_SIZE = 30
TOTAL_QUESTIONS = len(ALL_QUESTIONS)
TOTAL_SECTIONS = (TOTAL_QUESTIONS + SECTION_SIZE - 1) // SECTION_SIZE

def get_question_markup(question):
    buttons = []
    for key, val in question["javoblar"].items():
        buttons.append([InlineKeyboardButton(text=f"{key}) {val}", callback_data=key)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message_handler(commands=["start"])
async def start_test(message: types.Message):
    user_id = message.from_user.id
    USER_STATE[user_id] = {
        "index": 0,
        "score": 0,
        "wrong": 0,
        "section": 0,
        "paused": False
    }
    await send_next_question(message.chat.id, user_id)

@dp.message_handler(commands=["pause"])
async def pause_test(message: types.Message):
    user_id = message.from_user.id
    if user_id in USER_STATE:
        USER_STATE[user_id]["paused"] = True
        await message.answer("⏸ Test to‘xtatildi.")
    else:
        await message.answer("Siz testni hali boshlamadingiz.")

@dp.message_handler(commands=["resume"])
async def resume_test(message: types.Message):
    user_id = message.from_user.id
    if user_id in USER_STATE:
        USER_STATE[user_id]["paused"] = False
        await message.answer("▶ Test davom ettirilmoqda.")
        await send_next_question(message.chat.id, user_id)
    else:
        await message.answer("Siz testni hali boshlamadingiz.")

async def send_next_question(chat_id, user_id):
    user_data = USER_STATE.get(user_id)
    if not user_data:
        return
    idx = user_data["index"]

    question = ALL_QUESTIONS[idx]
    markup = get_question_markup(question)
    await bot.send_message(chat_id, f"🧪 Savol {idx + 1}:\n\n{question['savol']}", reply_markup=markup)

    seconds = 0
    while seconds < 30:
        if user_data["paused"]:
            await asyncio.sleep(1)
            continue
        await asyncio.sleep(1)
        seconds += 1

    user_data = USER_STATE.get(user_id)
    if user_data and user_data["index"] == idx and not user_data["paused"]:
        user_data["index"] += 1
        user_data["wrong"] += 1
        await send_next_question(chat_id, user_id)

@dp.callback_query_handler()
async def handle_answer(callback: types.CallbackQuery):
    if callback.data not in ["A", "B", "C", "D"]:
        await callback.answer()
        return

    user_id = callback.from_user.id
    user_data = USER_STATE.get(user_id)

    if not user_data:
        await callback.message.answer("Iltimos, /start buyrug‘idan boshlang.")
        await callback.answer()
        return

    idx = user_data["index"]
    section = user_data["section"]
    start_idx = section * SECTION_SIZE

    question = ALL_QUESTIONS[start_idx + idx]

    if callback.data == question["togri_javob"]:
        await callback.message.answer("✅ To‘g‘ri javob!")
        user_data["score"] += 1
    else:
        togri = question["togri_javob"]
        await callback.message.answer(f"❌ Noto‘g‘ri. To‘g‘ri javob: {togri}) {question['javoblar'][togri]}")
        user_data["wrong"] += 1

    user_data["index"] += 1
    await send_next_question(callback.message.chat.id, user_id)
    await callback.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
