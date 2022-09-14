from aiogram import types
from aiogram.fsm.context import FSMContext

from tgbot.loader import config, bot
from tgbot.keyboards import admin_menu
from tgbot.routers import admin_router
from aiogram.filters import Text

from tgbot.utils import states
from tgbot.utils.admin_functions import send_file_to_users, get_rcopy_database, get_admins_details, \
    replan_rcopy_database

router = admin_router


# Open reserve copies menu
@router.callback_query(Text(text='reserve_copies'))
async def open_storage_center(call: types.CallbackQuery):
    text = '<b>🗃 Настройка резервного копирования</b>'
    markup = admin_menu.reserve_copies(config.misc.rcopy_pauses.database)
    await call.message.answer(text=text, reply_markup=markup)


# Set pause beetween sendings of reserve copies
@router.callback_query(Text(text_startswith='set_rcopy_pause_'))
async def set_rcopy_pause(call: types.CallbackQuery):
    name, value = call.data.replace('set_rcopy_pause_', '').split('_')
    config.misc.rcopy_pauses[name] = int(value)
    config.save()
    markup = admin_menu.reserve_copies(config.misc.rcopy_pauses.database)

    try:
        await call.message.edit_reply_markup(reply_markup=markup)
        replan_rcopy_database()
        text = '✅ Успешно изменено!'

    except:
        text = '⚠ Что-то пошло не так!'

    await call.answer(text=text, show_alert=True)


# Download reserve copy of choosen stuff
@router.callback_query(Text(text_startswith='download_'))
async def download(call: types.CallbackQuery):
    data = {'database': get_rcopy_database}[call.data.replace('download_', '')]()
    await send_file_to_users(bot, [call.from_user.id], data)


# Open admin menu
@router.callback_query(Text(text='admins'))
async def open_admins(call: types.CallbackQuery):
    text = '<b>👨‍❤️‍👨 Вот текущий админ состав</b>'
    admins = await get_admins_details()
    await call.message.answer(text=text, reply_markup=admin_menu.admins(admins))


# Start adding of new admin
@router.callback_query(Text(text='add_admin'))
async def add_admin(call: types.CallbackQuery, state: FSMContext):
    text = '<b>✏ Введите id нового админа!</b>'

    await call.message.answer(text=text, reply_markup=admin_menu.cancel())
    await state.set_state(states.Admin.adding_admin)


# Get id of new admin and react on it
@router.message(state=states.Admin.adding_admin)
async def add_admin(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.delete()

    if msg.text.isdigit():
        admin_id = int(msg.text)
        try:
            if await bot.get_chat(chat_id=admin_id) is None:
                raise Exception
            if admin_id in config.bot.admins:
                text = '<b>⚠ Нельзя добавить пользователя в админы, если он итак уже админ!</b>'
            else:
                config.bot.admins.append(admin_id)
                config.save()
                text = '<b>✅ Админ успешно добавлен!</b>'
        except:
            text = '<b>⚠ Некорректный id!</b>'
    else:
        text = '<b>Некорректный id!</b>'

    await msg.answer(text=text, reply_markup=admin_menu.close())


# Delete admin from admin list
@router.callback_query(Text(text_startswith='delete_admin_'))
async def delete_admin(call: types.CallbackQuery):
    admin_id = int(call.data.replace('delete_admin_', ''))

    if admin_id in config.bot.admins:
        if admin_id == call.from_user.id:
            text = '⚠ Вы не можете удалить самого себя из админ состава!'
        elif config.bot.admins.index(admin_id) < config.bot.admins.index(call.from_user.id):
            text = '⚠ Вы не можете удалить того, кто находится выше вас!'
        else:
            text = '✅ Админ успешно удалён!'
    else:
        text = '⚠ Что-то пошло не так!'
    await call.answer(text=text, show_alert=True)

    text = '<b>👨‍❤️‍👨 Вот текущий админ состав</b>'
    try:
        await call.message.edit_text(text=text, reply_markup=admin_menu.admins(await get_admins_details()))
    except:
        pass
