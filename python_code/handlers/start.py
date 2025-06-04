from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import CommandStart

from Database.tables import Users, user_session
import re

start_router = Router()
class Reg(StatesGroup):
    ism = State()
    familya = State()
    username = State()
    phone = State()
    email = State()
    address = State()

@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if user := Users.get_by_id(user_session, message.chat.id) is None:
        await message.answer("Ismingizni kiriting")
        await state.set_state(Reg.ism)
    await message.answer(user.greating)



@start_router.message(Reg.ism)
async def firstname(message: Message, state:FSMContext):
    if not message.text.isalpha():
        await message.answer(f"Ismda faqat harflar ishtirok etishi kerak")
        return
    if len(message.text) > 50:
        await message.answer(f"50ta harfdan kam bo'lish kerak")

    ism = message.text.capitalize()
    await state.update_data(first_name=ism)
    await message.answer(f"Familyangizni kiriting")
    await state.set_state(Reg.familya)

@start_router.message(Reg.familya)
async def lastname(message: Message, state:FSMContext):
    if not message.text.isalpha():
        await message.answer(f"Familiyada faqat harflar ishtirok etishi kerak")
        return
    if len(message.text) > 50:
        await message.answer(f"50ta harfdan kam bo'lish kerak")


    familiya = message.text.capitalize()
    await state.update_data(last_name=familiya)

    keyboard = [[KeyboardButton(text="Kontaktni ulashish", request_contact=True)]]

    await message.answer(f"Kontakt tashlang", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
    await state.set_state(Reg.phone)

@start_router.message(Reg.phone)
async def phone(message: Message, state:FSMContext):
    if message.contact and len(str(message.contact.phone_number)) > 13:
        await message.answer(f"uzunligi 13 bo'lish kerak")
        return
    await state.update_data(phone=str(message.contact.phone_number))

    data = await state.get_data()
    user = Users(chat_id=message.chat.id, firstname=data["first_name"], lastname=data["last_name"],
                 phone=data["phone"])
    user.save(session=user_session)
    await state.clear()
    await message.answer(f"Registratsiya qilganingiz uchun raxmat, botdan foydalanishingiz mumkin😊")


