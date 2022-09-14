from tgbot.handlers.admin.mail import router, Text, admin_menu, types
from tgbot.handlers.admin.functions import router


@router.message(Text(text='/admin'), state='*')
async def open_admin_menu(msg: types.Message):
    text = '<b>👑 Админ-меню</b>'
    await msg.answer(text=text, reply_markup=admin_menu.main())
