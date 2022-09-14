import datetime
from aiogram import types, Bot

from config import Consts
from tgbot.keyboards import admin_menu
from tgbot.loader import bot, scheduler, config
from tgbot.services.api_database import User
from tgbot.utils.misc_functions import sdelete


# Conduct a mailing
async def mail(mailer_id: int, state_data: dict):
    success, total = 0, 0
    s_time = datetime.datetime.now()

    msg = state_data['msg']
    button = types.InlineKeyboardButton(text='👁 Закрыть', callback_data='close')
    markup = admin_menu.updated(msg.reply_markup, button) if state_data['need_button'] else msg.reply_markup

    for user in User.get_all(User.id):
        user_id = user['id']
        total += 1
        try:
            await msg.copy_to(chat_id=user_id, reply_markup=markup)
            success += 1
        except:
            ...
    e_time = datetime.datetime.now()
    during = round((e_time - s_time).total_seconds(), 3)
    s_percent = round((success / total) * 100, 2)
    text = f'<b>📊 Отчёт о проведённой рассылке</b>\n\n' \
           f'<i>⏰ Длительность:</i> <code>{during} сек</code>\n' \
           f'<i>✅ Успешность:</i> <code>{s_percent}%</code>\n' \
           f'<i>👤 Охват:</i> <code>{total}</code>'
    await bot.send_message(chat_id=mailer_id, text=text)


# Plan mailing on the time
def plan_mail(mailer_id: int, state_data: dict, dt: datetime.datetime):
    return scheduler.add_job(
        func=mail,
        trigger='date',
        run_date=dt,
        name='mail',
        timezone='Europe/Moscow',
        kwargs=dict(
            state_data=state_data,
            mailer_id=mailer_id
        ))


# Return planned mailings
def get_planned_mails() -> list[str, datetime.datetime]:
    return [(job.id, job.next_run_time) for job in scheduler.get_jobs(jobstore='default') if job.name == 'mail']


# Return reserve copy of database
def get_rcopy_database() -> types.FSInputFile:
    from shutil import copy
    dst = Consts.database_file + '.copy'
    sdelete(dst)
    copy(Consts.database_file, dst)
    return types.FSInputFile(dst, filename='rdatabase.db')


# Send the file to list of users
async def send_file_to_users(_bot: Bot, user_ids: list[int], file: types.InputFile):
    for user_id in user_ids:
        try:
            await bot.send_document(chat_id=user_id, document=file)
        except:
            pass


# Change pause beetween mailings
def replan_rcopy_database():
    job_id = 'rcopy_database'
    if scheduler.get_job(job_id=job_id) is None:
        kwargs = {'_bot': bot, 'user_ids': config.bot.admins, 'file': get_rcopy_database()}
        scheduler.add_job(
            id=job_id,
            func=send_file_to_users,
            trigger='interval',
            minutes=config.misc.rcopy_pauses.database,
            kwargs=kwargs,
            next_run_time=datetime.datetime.now())
    else:
        scheduler.reschedule_job(job_id=job_id, trigger='interval', minutes=config.misc.rcopy_pauses.database)


# Return details about admins
async def get_admins_details():
    admins = []
    for i in config.bot.admins:
        user_id, username = i, 'none'
        try:
            admin = await bot.get_chat(chat_id=i)
            user_id, username = admin.id, admin.username
        except:
            pass
        admins.append((user_id, username))
    return admins
