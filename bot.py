import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8888145721:AAFsvpIxWmKjYxShoaokNk8Sp0b2gIFU"  # Ваш реальный токен
ADMIN_ID = 893634915

# ===== ЛОГИРОВАНИЕ =====
logging.basicConfig(level=logging.INFO)

# ===== БОТ =====
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== ТЕКСТЫ =====
MENU_TEXT = """
Добро пожаловать в Lolz Deals 🎉

Ваш надежный P2P-гарант:
1. Автоматические сделки с NFT и подарками
2. Полная защита обеих сторон
3. Реферальная программа — 50% от комиссии
4. Передача товаров через менеджера: @Lolz_Deals
"""

# ===== КЛАВИАТУРЫ =====
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мои реквизиты", callback_data="requisites")],
        [InlineKeyboardButton(text="Создать сделку", callback_data="create_deal")],
        [InlineKeyboardButton(text="Баланс", callback_data="balance")],
        [InlineKeyboardButton(text="Мои сделки", callback_data="my_deals")],
        [InlineKeyboardButton(text="Рефералы", callback_data="referrals")],
        [InlineKeyboardButton(text="Язык / Lang", callback_data="lang")],
        [InlineKeyboardButton(text="Отзывы", callback_data="reviews")],
        [InlineKeyboardButton(text="Техподдержка", callback_data="support")]
    ])
    return keyboard

# ===== КОМАНДА /start =====
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(MENU_TEXT, reply_markup=get_main_keyboard())

# ===== ОБРАБОТЧИКИ КНОПОК =====
@dp.callback_query(lambda c: c.data == "requisites")
async def requisites(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "💰 Ваши реквизиты: BTC, USDT, ETH.\nПодробнее у @Lolz_Deals",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "create_deal")
async def create_deal(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📝 Создание сделки:\n1. Укажите сумму\n2. Выберите валюту\n3. Ожидайте менеджера @Lolz_Deals",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "balance")
async def balance(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "💳 Ваш баланс:\nОсновной: 0.00 USDT\nБонусный: 0.00 USDT\nЗаморожено: 0.00 USDT",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "my_deals")
async def my_deals(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📋 Список ваших сделок:\nАктивных: 0\nЗавершённых: 0\nОжидают: 0",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "referrals")
async def referrals(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "👥 Реферальная программа:\nПриглашено: 0\nЗаработано: 0.00 USDT\nКомиссия: 50%",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "lang")
async def lang(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🌐 Выберите язык:\n🇷🇺 Русский\n🇬🇧 English",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "reviews")
async def reviews(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "⭐ Отзывы:\n★★★★★ (5.0) — 127 отзывов\n🟢 Положительные: 98%",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "support")
async def support(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🛠 Техподдержка:\n📌 @Lolz_Deals\nВремя работы: 24/7",
        reply_markup=get_main_keyboard()
    )

# ===== ЗАПУСК =====
async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
