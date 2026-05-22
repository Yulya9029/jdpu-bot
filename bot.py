import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# =====================
# TOKEN (Render uchun)
# =====================
TOKEN = os.getenv("TOKEN")

# =====================
# BOT + DISPATCHER
# =====================
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# =====================
# MENU
# =====================
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📩 Отправить обращение")],
        [KeyboardButton(text="ℹ️ Помощь")]
    ],
    resize_keyboard=True
)

# =====================
# START COMMAND
# =====================
@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "👋 Assalomu alaykum!\n\nXotin-qizlar himoya botiga xush kelibsiz.",
        reply_markup=menu
    )

# =====================
# HELP
# =====================
@dp.message(F.text == "ℹ️ Помощь")
async def help_cmd(message: Message):
    await message.answer(
        "📌 Bu bot orqali murojaat yuborishingiz mumkin."
    )

# =====================
# REQUEST START
# =====================
@dp.message(F.text == "📩 Отправить обращение")
async def request(message: Message):
    await message.answer(
        "✍️ Iltimos, murojaatingizni yozing."
    )

# =====================
# SAVE MESSAGE + SEND TO ADMIN GROUP
# =====================
ADMIN_CHAT_ID = -1003965403672  # <-- sizning group ID (minus bilan!)

@dp.message(F.text)
async def all_messages(message: Message):
    user_id = message.from_user.id
    username = message.from_user.full_name
    text = message.text

    # ===== FILEGA YOZISH =====
    with open("appeals.txt", "a", encoding="utf-8") as f:
        f.write(f"ID: {user_id}\n")
        f.write(f"Ism: {username}\n")
        f.write(f"Murojaat: {text}\n")
        f.write("-" * 30 + "\n")

    # ===== ADMIN GURUHGA YUBORISH =====
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📩 Yangi murojaat:\n\n👤 {username}\n🆔 {user_id}\n💬 {text}"
    )

    # ===== USERGA JAVOB =====
    await message.answer("✅ Murojaatingiz qabul qilindi!")

# =====================
# MAIN
# =====================
async def main():
    print("BOT IS RUNNING...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())