import datetime
import validators

from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from calendagram import DatetimeManager

from tgbot.loader import scheduler, bot
from tgbot.routers import admin_router
from tgbot.keyboards import admin_menu
from tgbot.utils import states
from tgbot.utils.admin_functions import mail, plan_mail, get_planned_mails

router = admin_router


# Open mailing menu
@router.callback_query(Text(text='mailing_center'), state='*')
async def open_mailing_center(call: types.CallbackQuery):
    text = '<b>📫 Меню для управления рассылками</b>'
    planned_count = len(get_planned_mails())
    await call.message.answer(text=text, reply_markup=admin_menu.mailing_center(planned_count))


# Start mailing process
@router.callback_query(Text(text='get_message_for_mail'), state='*')
async def get_message_for_mail(call: types.CallbackQuery, state: FSMContext):
    text = '<b>⤴ Ответьте на сообщение, которое будет использоваться в рассылке, любым текстом</b>'
    await call.message.answer(text=text, reply_markup=admin_menu.cancel())
    await state.set_state(states.Admin.mailing)


# Get message for mailing
@router.message(state=states.Admin.mailing)
async def get_msg_for_mailing(msg: types.Message, state: FSMContext):
    if msg.reply_to_message is None:
        text = '<b>⚠ На желаемое сообщение нужно ответить!</b>'
        markup = admin_menu.close()
        await state.clear()
    else:
        text = '<b>🧐 Нужна ли кнопка для закрытия сообщения рассылки?</b>'
        markup = admin_menu.ask_button()
        await state.update_data(msg=msg.reply_to_message)
    await msg.delete()
    await msg.answer(text=text, reply_markup=markup)


# Ask for adding button to mailing message
@router.callback_query(Text(text_startswith='need_button_'), state=states.Admin.mailing)
async def get_message_for_mail(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(need_button=call.data.endswith('yes'))
    text = '<b>🧭 Когда вы хотите провести рассылку?</b>'
    markup = admin_menu.mailing_types()
    await call.message.answer(text=text, reply_markup=markup)


# Start mailing right now
@router.callback_query(Text(text='start_mailing_now'), state=states.Admin.mailing)
async def choose_type_of_mailing(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await mail(mailer_id=call.from_user.id, state_data=await state.get_data())
    await state.clear()


# Start choosing time for mailing
async def planing_mail(msg: types.Message, state: FSMContext):
    dt = await DatetimeManager.get_datetime(text=msg.text, state=state)
    markup = admin_menu.close()
    error_text = '<b>⚠ Некорректное время! Попробуйте ещё раз!</b>'
    if dt is None:
        text = error_text
    elif dt < datetime.datetime.now():
        text = error_text
    else:
        job = plan_mail(mailer_id=msg.from_user.id, state_data=await state.get_data(), dt=dt)
        text = f'<b>✅ Рассылка успешно запланирована!</b>\n\n' \
               f'<b>⏰ Время проведения: <code>{dt}</code></b>\n' \
               f'<b>🆔 Индификатор: <code>{job.id}</code></b>'
        markup = admin_menu.planned_mail(job.id)
        await state.clear()
    await msg.answer(text=text, reply_markup=markup)


dt_manager = DatetimeManager(router, planing_mail)
router.callback_query.register(dt_manager.show_calendar_callback, Text(text='start_mailing_later'), states.Admin.mailing)


# Start adding of url button to message
@router.callback_query(Text(text='add_url_button'))
async def add_url_button(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(states.Admin.buttoning)
    text = '<b>⤴ Ответьте на сообщение, к которому хотите добавить url-кнопку, в формате: <code>текст|ссылка</code></b>'
    await call.message.answer(text=text, reply_markup=admin_menu.cancel())


# Get button data
@router.message(state=states.Admin.buttoning)
async def get_button_data(msg: types.Message, state: FSMContext):
    is_error = True
    await msg.delete()
    markup = admin_menu.close()
    if msg.reply_to_message is None:
        text = '<b>⚠ Нужно ответить на сообщение!</b>'

    elif '|' in msg.text:
        button_text, url = msg.text.split('|')

        if validators.url(url) is True:
            text = '<b>🧐 Куда добавить кнопку?</b>'
            markup = admin_menu.button_place()
            is_error = False
            await state.update_data(button=types.InlineKeyboardButton(text=button_text, url=url),
                                    msg=msg.reply_to_message)

        else:
            text = '<b>⚠ Некорректная ссылка!</b>'
    else:
        text = '<b>⚠ Введённый текст не соответствует шаблону!</b>'

    if is_error:
        await state.clear()

    await msg.answer(text=text, reply_markup=markup)


# Get row for adding of button
@router.callback_query(Text(text=('last_row', 'new_row')), state=states.Admin.buttoning)
async def choose_place(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg, button = data['msg'], data['button']
    markup = admin_menu.updated(msg.reply_markup, button, call.data == 'new_row')
    await msg.copy_to(chat_id=call.from_user.id, reply_markup=markup)
    await call.message.delete()
    await state.clear()


# Get list of planned mailings
@router.callback_query(Text(text='planned_mails'))
async def show_planned_mails(call: types.CallbackQuery):
    mails = get_planned_mails()
    if len(mails) == 0:
        text = '<b>❌ Рассылок не запланировано!</b>'
        markup = admin_menu.close()
    else:
        text = '<b>✉ Запланированные рассылки</b>\n\n' \
               '<i>⚠ Для просмотра сообщения нажмите на id или время рассылки!</i>'
        markup = admin_menu.planned_mails(mails)
    await call.message.answer(text=text, reply_markup=markup)


# Show planned mailing info
@router.callback_query(Text(text_startswith='show_mail_'))
async def show_mail(call: types.CallbackQuery):
    kwargs = scheduler.get_job(job_id=call.data.replace('show_mail_', '')).kwargs
    data = kwargs['state_data']
    mailer = kwargs['mailer_id']
    msg_id = (await data['msg'].copy_to(chat_id=call.from_user.id, reply_markup=None)).message_id

    text = f'<b>✉ Это сообщение, которое будет использовано</b>\n\n' \
           f'<b>👤 Инициатор: <code>id{mailer}</code></b>'
    markup = admin_menu.close(and_replied=True)

    await bot.send_message(text=text, reply_markup=markup, reply_to_message_id=msg_id, chat_id=call.from_user.id)


# Refresh list of planned mailings
async def reload_planned_mails(call: types.CallbackQuery):
    mails = get_planned_mails()
    if len(mails) == 0:
        text = '<b>❌ Рассылок не запланировано!</b>'
        markup = admin_menu.close()
    else:
        text = '<b>✉ Запланированные рассылки</b>\n\n' \
               '<i>⚠ Для просмотра сообщения нажмите на id или время рассылки!</i>'
        markup = admin_menu.planned_mails(mails)
    try:
        await call.message.edit_text(text=text, reply_markup=markup)
    except:
        pass


# Cancel planned mailing
@router.callback_query(Text(text_startswith=('cancel_mail_', 'cancel_mail2_')))
async def cancel_mail(call: types.CallbackQuery):
    job_id = call.data.replace('cancel_mail_', '')
    try:
        scheduler.remove_job(job_id=job_id)
    except:
        pass

    text = '✅ Рассылка успешно отменена!'
    await call.answer(text=text, show_alert=True)

    if call.data.startswith('cancel_mail_'):
        await reload_planned_mails(call)
    else:
        await call.message.delete()


# Just a handler
@router.callback_query(Text(text='reload_planned_mails'))
async def reload_mails(call: types.CallbackQuery):
    await reload_planned_mails(call)
