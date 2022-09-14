import datetime

from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton


# Return markup with cancel button
def cancel(text: str = '🚫 Отмена', and_replied: bool = False) -> InlineKeyboardMarkup:
    data = 'close'
    if and_replied:
        data += '_and_replied'
    markup = [
        [
            InlineKeyboardButton(text=text, callback_data=data)
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return markup with close button
def close(text: str = '✖ Закрыть', and_replied: bool = False) -> InlineKeyboardMarkup:
    data = 'close'
    if and_replied:
        data += '_and_replied'
    markup = [
        [
            InlineKeyboardButton(text=text, callback_data=data)
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return markup with main admin menu
def main() -> InlineKeyboardMarkup:
    markup = [
        [
            InlineKeyboardButton(text='📫 Рассылки', callback_data='mailing_center'),
            InlineKeyboardButton(text='👨‍❤️‍👨 Админ состав', callback_data='admins')
        ],
        [
            InlineKeyboardButton(text='📑 Резервное копирование', callback_data='reserve_copies')
        ],
        [
            InlineKeyboardButton(text='✖ Закрыть', callback_data='close')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return markup that manages mailings
def mailing_center(planned_count: int) -> InlineKeyboardMarkup:
    markup = [
        [
            InlineKeyboardButton(text='📨 Провести рассылку', callback_data='get_message_for_mail')
        ],
        [
            InlineKeyboardButton(text=f'🗂 Запланированные [{planned_count}]', callback_data='planned_mails')
        ],
        [
            InlineKeyboardButton(text='🔗 Добавить url-кнопку', callback_data='add_url_button')
        ],
        [
            InlineKeyboardButton(text='✖ Закрыть', callback_data='close')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return markup that can add close button to message
def ask_button() -> InlineKeyboardMarkup:
    markup = [
        [
            InlineKeyboardButton(text='➕ Добавить кнопку', callback_data='need_button_yes'),
            InlineKeyboardButton(text='❌ Не нужно', callback_data='need_button_no')
        ],
        [
            InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return markup that contains mailing types
def mailing_types() -> InlineKeyboardMarkup:
    markup = [
        [
            InlineKeyboardButton(text='⏳ Сейчас', callback_data='start_mailing_now'),
            InlineKeyboardButton(text='📅 Позже', callback_data='start_mailing_later')
        ],
        [
            InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return updated markup
def updated(markup: InlineKeyboardMarkup, button: InlineKeyboardButton, new_row: bool = True) -> InlineKeyboardMarkup:
    if markup is None:
        markup = []
    else:
        markup = markup.inline_keyboard
    if new_row:
        markup.append([button])
    else:
        if len(markup) == 0:
            markup.append([button])
        else:
            markup[len(markup)-1].append(button)
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return markup that contains choice of button place
def button_place():
    markup = [
        [
            InlineKeyboardButton(text='В последний ряд', callback_data='last_row'),
            InlineKeyboardButton(text='В новый ряд', callback_data='new_row')
        ],
        [
            InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return markup that contains planned mailings
def planned_mails(mails: list[str, datetime.datetime]):
    markup = [
        [
            InlineKeyboardButton(text='ID', callback_data='none'),
            InlineKeyboardButton(text='Время', callback_data='none'),
            InlineKeyboardButton(text='\t', callback_data='none')
        ],
        *[[
            InlineKeyboardButton(text=mail[0], callback_data=f'show_mail_{mail[0]}'),
            InlineKeyboardButton(text=str(mail[1]), callback_data=f'show_mail_{mail[0]}'),
            InlineKeyboardButton(text='🗑', callback_data=f'cancel_mail_{mail[0]}')
        ] for mail in mails],
        [
            InlineKeyboardButton(text='🔄 Обновить', callback_data='reload_planned_mails'),
            InlineKeyboardButton(text='✖ Закрыть', callback_data='close')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return markup that suggests cancel planned mailing
def planned_mail(mail_id):
    markup = [
        [
            InlineKeyboardButton(text='🗑 Отменить', callback_data=f'cancel_mail2_{mail_id}'),
            InlineKeyboardButton(text='✖ Закрыть', callback_data='close')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return markup that allows to manage reserve copies
def reserve_copies(database_selected):
    database_row = [InlineKeyboardButton(text='База данных', callback_data='download_database')]
    for i in [0.5, 1, 1.5]:
        if i * 60 == database_selected:
            text = f'• {i}ч •'
        else:
            text = f'{i}ч'
        database_row.append(InlineKeyboardButton(text=text, callback_data=f'set_rcopy_pause_database_{i * 60}'))

    markup = [
        [
            InlineKeyboardButton(text='Имя', callback_data='none'),
            InlineKeyboardButton(text='\t', callback_data='none'),
            InlineKeyboardButton(text='Пауза', callback_data='none'),
            InlineKeyboardButton(text='\t', callback_data='none'),
        ],
        database_row,
        [
            InlineKeyboardButton(text='✖ Закрыть', callback_data='close')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)


# Return markup that contains button for manage admin list
def admins(admin_list: list[tuple[int, str]]):
    markup = [
        *[[
            InlineKeyboardButton(text=f'id{i[0]}', callback_data='none'),
            InlineKeyboardButton(text=f'@{i[1]}', callback_data='none'),
            InlineKeyboardButton(text='🗑', callback_data=f'delete_admin_{i[0]}')
        ] for i in admin_list],
        [
            InlineKeyboardButton(text='➕ Добавить админа', callback_data='add_admin')
        ],
        [
            InlineKeyboardButton(text='✖ Закрыть', callback_data='close')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)
