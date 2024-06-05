import asyncio

from aiogram import Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile, CallbackQuery

from notification.models import Notification
from user.models import User

dispatcher = Dispatcher()


start_text = '''<b>Привет!</b>

Впереди тебя ждёт турнир по покеру с призовым фондом:
 
<b>5.000 руб.</b>

Для регистрации жми <b>🔥 ЗАРЕГИСТРИРОВАТЬСЯ 🔥!</b>
Чтобы узнать правила турнира, жми <b>📚 Правила 📚</b>

Через время я пришлю всю информацию по турниру, что, где и когда будет проходить...
'''

rules_text = '''📚 Правила 📚

1. Вход - 0 руб. (Играем на деньги компании)
2. Каждые 12 минут повышение блайндов в 2 раза (Минимальное количество фишек для ставки)
3. Начальные блайнды 10/20
4. Играем в техасский холдем
5. За каждого выбитого человека есть баунти, размером 100 руб. (Из призового фонда)
6. Принести с собой хорошее настроение

Удачной охоты, Сталкер!
'''


keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔥 ЗАРЕГИСТРИРОВАТЬСЯ 🔥', callback_data='register')],
                                                 [InlineKeyboardButton(text='📚 Правила 📚', callback_data='rules')]])

rules_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔥 ЗАРЕГИСТРИРОВАТЬСЯ 🔥', callback_data='register')]])
register_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='📚 Правила 📚', callback_data='rules')]])


@dispatcher.message(F.text, CommandStart())
async def echo(message: Message):
    with open('/app/rosources/poker_tournament.png', 'rb') as f:
        await message.answer_photo(photo=BufferedInputFile(f.read(), filename='poker.png'), caption=start_text,
                                   parse_mode=ParseMode.HTML, reply_markup=keyboard)


@dispatcher.callback_query(F.data)
async def callback(query: CallbackQuery):
    data = query.data
    match data:
        case 'register':
            with open('/app/rosources/poker_tournament_register.png', 'rb') as f:
                user = await asyncio.to_thread(User.objects.filter(telegram_id=str(query.from_user.id)).first)
                if user:
                    await query.bot.send_photo(chat_id=query.from_user.id,
                                               photo=BufferedInputFile(f.read(), filename='poker.png'),
                                               caption='Вы уже зарегистрированы на турнир, ждите оповещений...',
                                               reply_markup=register_keyboard)
                    return
                await asyncio.to_thread(User(telegram_id=str(query.from_user.id),
                                        password='123456',
                                        username=query.from_user.username or str(query.from_user.id),
                                        first_name=query.from_user.first_name or None,
                                        last_name=query.from_user.last_name or None).save)
                await query.bot.send_photo(chat_id=query.from_user.id, photo=BufferedInputFile(f.read(), filename='poker.png'), caption='Вы успешно зарегистрировались на турнир! Чуть позже я сообщу вам всю информацию по турниру!', reply_markup=register_keyboard)
        case 'rules':
            with open('/app/rosources/poker_tournament_rules.png', 'rb') as f:
                await query.bot.send_photo(chat_id=query.from_user.id, photo=BufferedInputFile(f.read(), filename='poker.png'), caption=rules_text, reply_markup=rules_keyboard)
        case '0706poker_yes':
            notification = await Notification.objects.select_related('message').filter(user__telegram_id=str(query.from_user.id),
                                                                                       message__message=query.message.text).afirst()

            actions_count = await Notification.objects.filter(message__message=query.message.text,
                                                              action=Notification.ActionType.ACCEPT).acount()
            print(notification.message.max_actions > actions_count)
            if notification.message.max_actions > actions_count or notification.action == Notification.ActionType.ACCEPT:
                if notification.action != Notification.ActionType.ACCEPT:
                    await query.bot.send_message(chat_id=query.from_user.id, text='Вы успешно зарегистрированы на покер в эту пятницу')
                    notification.action = Notification.ActionType.ACCEPT
                else:
                    await query.bot.send_message(chat_id=query.from_user.id,
                                                 text='Вы уже зарегистрированы на покер в эту пятницу')
            else:
                await query.bot.send_message(chat_id=query.from_user.id, text='Мы уже набрали максимальное число участников')

            await notification.asave(update_fields=['action'])

        case '0706poker_no':
            notification = await Notification.objects.filter(user__telegram_id=str(query.from_user.id),
                                                             message__message=query.message.text).afirst()
            notification.action = Notification.ActionType.DECLINE
            await query.bot.send_message(chat_id=query.from_user.id,
                                         text='Вы отказались от участия в эту пятницу')
            await notification.asave(update_fields=['action'])

    # try:
    #     await query.bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=None)
    # except Exception as e:
    #     print(e)

