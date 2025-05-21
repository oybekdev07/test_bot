# import json
# import random
# import asyncio
# import logging
# from aiogram import Bot, Dispatcher, types, F
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.filters import Command, CommandObject
#
# # Logging
# logging.basicConfig(level=logging.INFO)
#
# API_TOKEN = "7917728161:AAGrWOcdJG65W-PwBwwfNl4COu3w1furDlY"  # <-- Tokenni bu yerga qo‘ying
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()
#
# # JSON faylni o‘qish
# with open("json.file", "r", encoding="utf-8") as f:
#     ALL_QUESTIONS = json.load(f)
#
# # Javoblarni A-D bo‘yicha aralashtirish
# new_keys = ["A", "B", "C", "D"]
# for item in ALL_QUESTIONS:
#     if "javoblar" in item and "togri_javob" in item:
#         old_answers = item["javoblar"]
#         correct_key = item["togri_javob"]
#         correct_value = old_answers.get(correct_key)
#         if correct_value is None:
#             raise ValueError(f"Tog‘ri javob topilmadi: {item.get('savol', 'Nomalum')}")
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
# # Har bir foydalanuvchi uchun holat
# USER_STATE = {}  # user_id -> {index, score, wrong, section}
#
# # Savollar soni va bo‘lim o‘lchami
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
#     logging.info(f"{message.from_user.full_name} 1-bo‘limni boshladi.")
#     USER_STATE[message.from_user.id] = {
#         "index": 0,
#         "score": 0,
#         "wrong": 0,
#         "section": 0
#     }
#     await send_next_question(message.chat.id, message.from_user.id)
#
# @dp.message(Command(commands=[f"section{i+1}" for i in range(TOTAL_SECTIONS)]))
# async def handle_section(message: types.Message, command: CommandObject):
#     try:
#         section_num = int(command.command.replace("section", ""))
#         if section_num < 1 or section_num > TOTAL_SECTIONS:
#             await message.answer("Noto‘g‘ri bo‘lim raqami.")
#             return
#         USER_STATE[message.from_user.id] = {
#             "index": 0,
#             "score": 0,
#             "wrong": 0,
#             "section": section_num - 1
#         }
#         await send_next_question(message.chat.id, message.from_user.id)
#     except Exception as e:
#         await message.answer("Xatolik: " + str(e))
#
#
# async def send_next_question(chat_id, user_id):
#     user_data = USER_STATE.get(user_id)
#     if not user_data:
#         return
#
#     idx = user_data["index"]
#     section = user_data["section"]
#     start_idx = section * SECTION_SIZE
#     end_idx = min(start_idx + SECTION_SIZE, TOTAL_QUESTIONS)
#
#     if start_idx + idx >= end_idx:
#         correct = user_data["score"]
#         wrong = user_data["wrong"]
#         section_number = section + 1
#         next_section = section_number + 1
#
#         text = (
#             f"✅ {section_number}-bo‘lim tugadi.\n"
#             f"To‘g‘ri javoblar: {correct} ta\n"
#             f"Noto‘g‘ri javoblar: {wrong} ta\n\n"
#         )
#
#         if end_idx < TOTAL_QUESTIONS:
#             text += f"➡️ {next_section}-bo‘limni boshlash uchun /section{next_section} buyrug‘ini bosing."
#         else:
#             text += f"🎉 Test yakunlandi!"
#
#         await bot.send_message(chat_id, text)
#         USER_STATE.pop(user_id)
#         return
#
#     question = ALL_QUESTIONS[start_idx + idx]
#     msg = f"🧪 {start_idx + idx + 1}-savol:\n\n{question['savol']}"
#     markup = get_question_markup(question)
#
#     await bot.send_message(chat_id, msg, reply_markup=markup)
#
#     # 30 soniya kutish
#     await asyncio.sleep(30)
#
#     # Agar javob bermagan bo‘lsa
#     user_data_after = USER_STATE.get(user_id)
#     if user_data_after and user_data_after["index"] == idx:
#         await bot.send_message(chat_id, "⏰ Vaqt tugadi! Keyingi savolga o‘tamiz.")
#         user_data_after["index"] += 1
#         user_data_after["wrong"] += 1
#         await send_next_question(chat_id, user_id)
#
#
# @dp.callback_query(F.data.in_(["A", "B", "C", "D"]))
# async def handle_answer(callback: types.CallbackQuery):
#     user_id = callback.from_user.id
#     user_data = USER_STATE.get(user_id)
#
#     if not user_data:
#         await callback.message.answer("Iltimos, /start buyrug‘idan boshlang.")
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
#
# if __name__ == "__main__":
#     asyncio.run(dp.start_polling(bot))

import json
import random
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, CommandObject

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Token
API_TOKEN = "917728161:AAGrWOcdJG65W-PwBwwfNl4COu3w1furDlY"  # <-- o'z tokeningizni shu yerga yozing
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# JSON fayldan testlarni yuklash
with open("json.file", "r", encoding="utf-8") as f:
    ALL_QUESTIONS = json.load(f)

# Javoblarni A-D tartibida aralashtirish
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

# Har bir foydalanuvchi uchun holat
USER_STATE = {}  # user_id -> {index, score, wrong, section}

# Savollar bo‘limi
SECTION_SIZE = 30
TOTAL_QUESTIONS = len(ALL_QUESTIONS)
TOTAL_SECTIONS = (TOTAL_QUESTIONS + SECTION_SIZE - 1) // SECTION_SIZE

# Tugmalarni yaratish
def get_question_markup(question):
    buttons = []
    for key, val in question["javoblar"].items():
        buttons.append([InlineKeyboardButton(text=f"{key}) {val}", callback_data=key)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# /start buyrug‘i
@dp.message(Command("start"))
async def start_test(message: types.Message):
    logging.info(f"{message.from_user.full_name} 1-bo‘limni boshladi.")
    USER_STATE[message.from_user.id] = {
        "index": 0,
        "score": 0,
        "wrong": 0,
        "section": 0
    }
    await send_next_question(message.chat.id, message.from_user.id)

# /section1, /section2, ... buyrug‘ini tutish
@dp.message(Command(commands=[f"section{i+1}" for i in range(TOTAL_SECTIONS)]))
async def handle_section(message: types.Message, command: CommandObject):
    try:
        section_num = int(command.command.replace("section", ""))
        if section_num < 1 or section_num > TOTAL_SECTIONS:
            await message.answer("Noto‘g‘ri bo‘lim raqami.")
            return
        USER_STATE[message.from_user.id] = {
            "index": 0,
            "score": 0,
            "wrong": 0,
            "section": section_num - 1
        }
        await send_next_question(message.chat.id, message.from_user.id)
    except Exception as e:
        await message.answer("Xatolik: " + str(e))

# Keyingi savolni yuborish
async def send_next_question(chat_id, user_id):
    user_data = USER_STATE.get(user_id)
    if not user_data:
        return

    idx = user_data["index"]
    section = user_data["section"]
    start_idx = section * SECTION_SIZE
    end_idx = min(start_idx + SECTION_SIZE, TOTAL_QUESTIONS)

    if start_idx + idx >= end_idx:
        correct = user_data["score"]
        wrong = user_data["wrong"]
        section_number = section + 1
        next_section = section_number + 1

        text = (
            f"✅ {section_number}-bo‘lim tugadi.\n"
            f"To‘g‘ri javoblar: {correct} ta\n"
            f"Noto‘g‘ri javoblar: {wrong} ta\n\n"
        )

        if end_idx < TOTAL_QUESTIONS:
            text += f"➡️ Keyingi bo‘limni boshlash: /section{next_section}"
        else:
            text += "🎉 Test yakunlandi! Rahmat."

        await bot.send_message(chat_id, text)
        USER_STATE.pop(user_id)
        return

    question = ALL_QUESTIONS[start_idx + idx]
    msg = f"🧪 {start_idx + idx + 1}-savol:\n\n{question['savol']}"
    markup = get_question_markup(question)

    await bot.send_message(chat_id, msg, reply_markup=markup)

    # 30 soniya kutish
    await asyncio.sleep(30)

    # Agar javob berilmagan bo‘lsa
    user_data_after = USER_STATE.get(user_id)
    if user_data_after and user_data_after["index"] == idx:
        await bot.send_message(chat_id, "⏰ Vaqt tugadi! Keyingisiga o‘tamiz.")
        user_data_after["index"] += 1
        user_data_after["wrong"] += 1
        await send_next_question(chat_id, user_id)

# Tugma bosilganda javobni tekshirish
@dp.callback_query()
async def handle_answer(callback: types.CallbackQuery):
    if callback.data not in ["A", "B", "C", "D"]:
        return

    user_id = callback.from_user.id
    user_data = USER_STATE.get(user_id)

    if not user_data:
        await callback.message.answer("Iltimos, /start buyrug‘idan boshlang.")
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

# Botni ishga tushurish
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
