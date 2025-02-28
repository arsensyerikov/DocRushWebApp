import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv
import os

# Завантажуємо змінні середовища
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Ініціалізація бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher()

# 📌 Підключення до бази даних SQLite
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 📌 Створення таблиць, якщо вони ще не існують
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    description TEXT,
    pickup_address TEXT,
    delivery_address TEXT,
    deadline TEXT,
    status TEXT DEFAULT 'Очікує підтвердження',
    payment_status TEXT DEFAULT 'Не оплачено'
)
""")
conn.commit()

# 🔹 FSM для створення замовлення
class OrderForm(StatesGroup):
    waiting_for_description = State()
    waiting_for_pickup = State()
    waiting_for_delivery = State()
    waiting_for_deadline = State()

@dp.message(Command("start"))
async def start(message: types.Message):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (message.from_user.id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (user_id, username, role) VALUES (?, ?, ?)", 
                       (message.from_user.id, message.from_user.username or "Невідомий", "user"))
        conn.commit()
        await message.answer("Ви успішно зареєстровані! 🎉")
    else:
        await message.answer("Ви вже зареєстровані! ✅")

@dp.message(Command("admin"))
async def admin(message: types.Message):
    parts = message.text.split()
    if len(parts) != 2 or parts[1] != "1320":
        await message.answer("❌ Неправильний код. Використання: `/admin 1320`")
        return

    cursor.execute("UPDATE users SET role = 'admin' WHERE user_id = ?", (message.from_user.id,))
    conn.commit()
    await message.answer("✅ Ви стали адміністратором (кур'єром)!")

@dp.message(Command("add_order"))
async def add_order(message: types.Message, state: FSMContext):
    cursor.execute("SELECT role FROM users WHERE user_id = ?", (message.from_user.id,))
    user_role = cursor.fetchone()

    if user_role and user_role[0] == "admin":
        await message.answer("❌ Кур'єри (адміни) не можуть створювати замовлення!")
        return

    await message.answer("📝 *Напишіть опис документа:*")
    await state.set_state(OrderForm.waiting_for_description)

@dp.message(OrderForm.waiting_for_description)
async def process_order_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    await message.answer("📍 *Де потрібно забрати документ?* (Введіть адресу)")
    await state.set_state(OrderForm.waiting_for_pickup)

@dp.message(OrderForm.waiting_for_pickup)
async def process_order_pickup(message: types.Message, state: FSMContext):
    await state.update_data(pickup_address=message.text.strip())
    await message.answer("📍 *Куди потрібно доставити документ?* (Введіть адресу)")
    await state.set_state(OrderForm.waiting_for_delivery)

@dp.message(OrderForm.waiting_for_delivery)
async def process_order_delivery(message: types.Message, state: FSMContext):
    await state.update_data(delivery_address=message.text.strip())
    await message.answer("⏳ *Вкажіть крайній час доставки (формат: HH:MM або 'будь-коли')*")
    await state.set_state(OrderForm.waiting_for_deadline)

@dp.message(OrderForm.waiting_for_deadline)
async def process_order_deadline(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    deadline = message.text.strip()

    cursor.execute("""
        INSERT INTO orders (user_id, description, pickup_address, delivery_address, deadline) 
        VALUES (?, ?, ?, ?, ?)""",
        (message.from_user.id, user_data["description"], user_data["pickup_address"], user_data["delivery_address"], deadline))
    conn.commit()

    await message.answer(
        f"✅ *Ваше замовлення додано!*\n"
        f"📄 *Опис:* {user_data['description']}\n"
        f"📍 *Забрати:* {user_data['pickup_address']}\n"
        f"📍 *Доставити:* {user_data['delivery_address']}\n"
        f"⏳ *Крайній час:* {deadline}"
    )
    await state.clear()

@dp.message(Command("orders"))
async def orders(message: types.Message):
    cursor.execute("SELECT role FROM users WHERE user_id = ?", (message.from_user.id,))
    user_role = cursor.fetchone()

    if not user_role:
        await message.answer("❌ Помилка доступу. Ви не зареєстровані.")
        return

    if user_role[0] == "admin":
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        response = "📋 *Всі замовлення користувачів:*\n"
    else:
        cursor.execute("SELECT * FROM orders WHERE user_id = ?", (message.from_user.id,))
        orders = cursor.fetchall()
        response = "📋 *Ваші замовлення:*\n"

    if orders:
        for order in orders:
            response += (
                f"🔹 *ID:* {order[0]}\n"
                f"   📄 *Опис:* {order[2]}\n"
                f"   📍 *Забрати:* {order[3]}\n"
                f"   📍 *Доставити:* {order[4]}\n"
                f"   ⏳ *Крайній час:* {order[5]}\n"
                f"   📦 *Статус:* {order[6]}\n"
                f"   💳 *Оплата:* {order[7]}\n\n"
            )
    else:
        response += "ℹ️ Немає доступних замовлень."

    await message.answer(response)

async def main():
    await dp.start_polling(bot)

@dp.message(Command("update_order"))
async def update_order(message: types.Message):
    cursor.execute("SELECT role FROM users WHERE user_id = ?", (message.from_user.id,))
    user_role = cursor.fetchone()

    if not user_role or user_role[0] != "admin":
        await message.answer("❌ Лише кур'єр може змінювати статус замовлення!")
        return

    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("❌ Використання: `/update_order <ID> <новий статус>`")
        return

    order_id, new_status = parts[1], parts[2]

    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()

    if not order:
        await message.answer("❌ Замовлення не знайдено!")
        return

    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()

    user_id = order[1]

    if new_status == "Доставлено":
        cursor.execute("UPDATE orders SET payment_status = 'Очікує оплату' WHERE id = ?", (order_id,))
        conn.commit()

        pay_button = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Оплачено", callback_data=f"pay_{order_id}")]
        ])

        await bot.send_message(
            user_id,
            f"📦 *Ваше замовлення #{order_id} доставлено!*\n"
            f"💳 *Сума до сплати:* 50 грн\n"
            f"💳 *Номер картки:* `4441111146829944`\n"
            "Перекажіть кошти на цю карту та натисніть 'Оплачено'.",
            reply_markup=pay_button
        )

    await message.answer(f"✅ Статус замовлення #{order_id} змінено на '{new_status}'")


@dp.callback_query(lambda query: query.data.startswith("pay_"))
async def confirm_payment_request(query: CallbackQuery):
    order_id = query.data.split("_")[1]

    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()

    if not order:
        await query.answer("❌ Замовлення не знайдено!")
        return

    admin = cursor.execute("SELECT user_id FROM users WHERE role = 'admin'").fetchone()
    if not admin:
        await query.answer("❌ Немає доступних адміністраторів!")
        return

    admin_id = admin[0]

    confirm_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Так", callback_data=f"confirm_{order_id}_yes"),
         InlineKeyboardButton(text="❌ Ні", callback_data=f"confirm_{order_id}_no")]
    ])

    await bot.send_message(
        admin_id,
        f"💰 *Користувач натиснув 'Оплачено' для замовлення #{order_id}.*\n"
        "Перевірте, чи кошти надійшли на карту.",
        reply_markup=confirm_buttons
    )

    await query.answer("Очікуємо підтвердження оплати адміністратором.")


@dp.callback_query(lambda query: query.data.startswith("confirm_"))
async def process_admin_payment_confirmation(query: CallbackQuery):
    try:
        print(f"DEBUG: Отримано callback - {query.data}")  # Лог для дебагу

        parts = query.data.split("_")

        if len(parts) < 3:  # Перевірка, чи є всі частини
            print(f"❌ DEBUG: Неправильний формат callback'а: {query.data}")
            await query.answer("❌ Помилка у форматі даних.")
            return

        order_id = parts[1]
        decision = parts[2]

        cursor.execute("SELECT user_id FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            await query.answer("❌ Замовлення не знайдено!")
            return

        user_id = order[0]  # Оновлено: правильний індекс для user_id

        if decision == "yes":
            cursor.execute("UPDATE orders SET payment_status = 'Оплачено' WHERE id = ?", (order_id,))
            conn.commit()

            await bot.send_message(user_id, f"✅ *Ваше замовлення #{order_id} успішно оплачено!*")
            await query.message.edit_text(f"✅ Оплата за замовлення #{order_id} підтверджена!")

            await query.answer("Оплата підтверджена!")

        elif decision == "no":
            pay_button = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Оплачено", callback_data=f"pay_{order_id}")]
            ])

            await bot.send_message(
                user_id,
                f"⚠️ *Ваш платіж за замовлення #{order_id} не підтверджено.*\n"
                "Будь ласка, перевірте переказ та натисніть 'Оплачено' ще раз.",
                reply_markup=pay_button
            )

            await query.message.edit_text(f"❌ Оплата за замовлення #{order_id} не підтверджена! Очікуємо повторний переказ.")
            await query.answer("Нагадування надіслано користувачу.")

    except Exception as e:
        print(f"❌ DEBUG: Помилка в confirm_ callback - {str(e)}")
        await query.answer("❌ Помилка в обробці. Перезапустіть бота.")





async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
