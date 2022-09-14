from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from tgbot.routers import user_router


router = user_router


@router.callback_query(Text(text=('close', 'close_and_replied')), state='*')
async def close(call: types.CallbackQuery):
    if call.message.reply_to_message is not None and 'replied' in call.data:
        try:
            await call.message.reply_to_message.delete()
        except:
            pass
    await call.message.delete()


@router.callback_query(Text(text=('cancel', 'cancel_and_replied')), state='*')
async def cancel(call: types.CallbackQuery, state: FSMContext):
    if call.message.reply_to_message is not None and 'replied' in call.data:
        try:
            await call.message.reply_to_message.delete()
        except:
            pass
    await call.message.delete()
    await state.clear()
