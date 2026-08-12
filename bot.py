import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8688145721:AAFsvpIwmMnWjYx5hbOaOKcN8SpOGbzg1FU"  # Замените на реальный
ADMIN_ID = 8936341915

# ===== ЛОГИРОВАНИЕ =====
logging.basicConfig(level=logging.INFO)

# ===== ХРАНИЛИЩЕ ДЛЯ FSM =====
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

# ===== СОСТОЯНИЯ =====
class RequisitesStates(StatesGroup):
    waiting_for_ton = State()

# ===== ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ (в памяти) =====
user_data = {}

# ===== INLINE-КНОПКИ ГЛАВНОГО МЕНЮ =====
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

# ===== INLINE-КНОПКИ ДЛЯ РЕКВИЗИТОВ =====
def get_requisites_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="TON-кошелёк", callback_data="req_ton")],
        [InlineKeyboardButton(text="BTC-кошелёк", callback_data="req_btc")],
        [InlineKeyboardButton(text="Карта", callback_data="req_card")],
        [InlineKeyboardButton(text="USDT-кошелёк", callback_data="req_usdt")],
        [InlineKeyboardButton(text="Stars", callback_data="req_stars")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
    ])
    return keyboard

# ===== ТЕКСТЫ =====
MENU_TEXT = """
Добро пожаловать в LoLz Deals 🎉

Ваш надежный P2P-гарант:
1. Автоматические сделки с NFT и подарками
2. Полная защита обеих сторон
3. Реферальная программа — 50% от комиссии
4. Передача товаров через менеджера: @LoLz_Deals
"""

def get_requisites_text(user_id):
    data = user_data.get(user_id, {})
    ton = data.get('ton', '–')
    btc = data.get('btc', '–')
    card = data.get('card', '–')
    usdt = data.get('usdt', '–')
    stars = data.get('stars', '@—')
    
    return f"""
Мои реквизиты

TON-кошелёк: {ton}
Карта: {card}
Stars: {stars}
USDT (TRC20): {usdt}
BTC: {btc}

изменено 20:12 🚩
"""

# ===== КОМАНДА /start =====
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(MENU_TEXT, reply_markup=get_main_keyboard())

# ===== ОБРАБОТЧИК "Мои реквизиты" =====
@dp.callback_query(lambda c: c.data == "requisites")
async def show_requisites(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    await callback.message.edit_text(
        get_requisites_text(user_id),
        reply_markup=get_requisites_keyboard()
    )

# ===== ОБРАБОТЧИК "TON-кошелёк" =====
@dp.callback_query(lambda c: c.data == "req_ton")
async def req_ton(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(RequisitesStates.waiting_for_ton)
    
    await callback.message.edit_text(
        "Введите новый TON-кошелёк:\n"
        "изменено 20:12\n\n"
        "Кошелёк должен начинаться с UQ или EQ (латиница, цифры, _ -).",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📎 Назад в меню", callback_data="back_to_main")]
        ])
    )

# ===== ВАЛИДАЦИЯ TON-АДРЕСА =====
def is_valid_ton_address(address: str) -> bool:
    if not address.startswith(('UQ', 'EQ')):
        return False
    if not re.match(r'^[A-Za-z0-9_\-]+$', address):
        return False
    if len(address) < 40:
        return False
    return True

# ===== ОБРАБОТКА ВВОДА TON =====
@dp.message(RequisitesStates.waiting_for_ton)
async def process_ton_input(message: types.Message, state: FSMContext):
    ton_address = message.text.strip()
    user_id = message.from_user.id
    
    if not is_valid_ton_address(ton_address):
        await message.answer(
            "❌ Неверный формат TON-кошелька.\n"
            "Кошелёк должен начинаться с UQ или EQ и содержать латиницу, цифры, _ или -.\n"
            "Попробуйте снова:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📎 Назад в меню", callback_data="back_to_main")]
            ])
        )
        return
    
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['ton'] = ton_address
    
    await state.clear()
    
    await message.answer(
        get_requisites_text(user_id),
        reply_markup=get_requisites_keyboard()
    )

# ===== ОСТАЛЬНЫЕ РЕКВИЗИТЫ (заглушки) =====
@dp.callback_query(lambda c: c.data == "req_btc")
async def req_btc(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Ваши реквизиты: BTC, USDT, ETH.\n"
        "Подробнее у @LoLz_Deals",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
        ])
    )

@dp.callback_query(lambda c: c.data == "req_card")
async def req_card(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Ваши реквизиты: BTC, USDT, ETH.\n"
        "Подробнее у @LoLz_Deals",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
        ])
    )

@dp.callback_query(lambda c: c.data == "req_usdt")
async def req_usdt(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Ваши реквизиты: BTC, USDT, ETH.\n"
        "Подробнее у @LoLz_Deals",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
        ])
    )

@dp.callback_query(lambda c: c.data == "req_stars")
async def req_stars(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Ваши реквизиты: BTC, USDT, ETH.\n"
        "Подробнее у @LoLz_Deals",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
        ])
    )

# ===== КНОПКА "НАЗАД В МЕНЮ" =====
@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(MENU_TEXT, reply_markup=get_main_keyboard())

# ===== ОСТАЛЬНЫЕ ОБРАБОТЧИКИ =====
@dp.callback_query(lambda c: c.data == "create_deal")
async def create_deal(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📝 Создание сделки:\n"
        "1. Укажите сумму\n"
        "2. Выберите валюту\n"
        "3. Ожидайте подтверждения менеджера @LoLz_Deals",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "balance")
async def balance(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "💳 Ваш баланс:\n"
        "Основной: 0.00 USDT\n"
        "Бонусный: 0.00 USDT\n"
        "Заморожено: 0.00 USDT",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "my_deals")
async def my_deals(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📋 Список ваших сделок:\n"
        "Активных: 0\n"
        "Завершённых: 0\n"
        "Ожидают подтверждения: 0",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "referrals")
async def referrals(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "👥 Реферальная программа:\n"
        "Ваша ссылка: https://t.me/ваш_бот?start=ref_ваш_id\n"
        "Приглашено: 0\n"
        "Заработано: 0.00 USDT\n"
        "Комиссия: 50% от каждой сделки реферала",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "lang")
async def lang(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🌐 Выберите язык:\n"
        "🇷🇺 Русский\n"
        "🇬🇧 English",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "reviews")
async def reviews(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "⭐ Отзывы о LoLz Deals:\n\n"
        "★★★★★ (5.0) — 127 отзывов\n"
        "🟢 Положительные: 98%\n\n"
        "Последние отзывы:\n"
        "✅ @user1: 'Быстро и надёжно!'\n"
        "✅ @user2: 'Лучший P2P-гарант'",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "support")
async def support(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🛠 Техподдержка LoLz Deals:\n\n"
        "Свяжитесь с менеджером:\n"
        "📌 @LoLz_Deals\n\n"
        "Время работы: 24/7\n"
        "Среднее время ответа: 5 минут",
        reply_markup=get_main_keyboard()
    )

# ===== ЗАПУСК =====
async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())