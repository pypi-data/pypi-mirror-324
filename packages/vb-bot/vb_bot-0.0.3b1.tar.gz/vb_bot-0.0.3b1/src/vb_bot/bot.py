import asyncio
import pickle
import traceback
from datetime import datetime
from logging import ERROR
import re
from random import uniform
from typing import Union, Literal, Callable, List
import mongoengine.errors
import telebot.types
from telebot.async_telebot import AsyncTeleBot
from time import time, sleep
from vb_bot.models.connector import connection
from vb_bot.models.api_queue import ApiQueue
from vb_bot.models.queue_callback import QueueCallback
from vb_bot.models.user import UserModel
from vb_bot.configs.telegram_api import config as tg_api
from vb_bot.configs.bot_settings import config as bot_config
from vb_bot.modules.setup_logger import special_logger


class TgBot(AsyncTeleBot):
    def __init__(self, token: str, database: str = "vb_tg", host: str = "localhost", port: int = 27017,
                 username: str = None, password: str = None, authentication_source: str = None, *args, **kwargs):
        super().__init__(token, *args, **kwargs)
        connection(database, host, port, username, password, authentication_source)
        self.daemons: List[Callable] = [self.sender]
        self.last_message_sent = time()
        self.errors_logger = special_logger("errors", ERROR, True)
        self.start_time = time()
        self.work_flag = True


    async def daemons_work(self):
        while self.work_flag:
            for func in self.daemons:
                await func()
            await asyncio.sleep(0.5)


    async def add_message_to_queue(self, user_id: int, text: Union[str, None] = None,
                                   message_id: Union[int, None] = None,
                                   reply_markup: Union[telebot.types.ReplyKeyboardMarkup,
                                                       telebot.types.InlineKeyboardMarkup, None] = None,
                                   parse_mode: Literal["HTML", "MARKDOWN"] = "HTML",
                                   action: Literal["send_message", "edit_message", "delete_message"] = "send_message",
                                   disable_notification: bool = False,
                                   **kwargs):
        try:
            user = UserModel.objects.get(user_id=user_id, block_bot=False, banned=False)
        except mongoengine.errors.DoesNotExist:
            return False

        new_queue_element = ApiQueue()
        new_queue_element.user = user
        new_queue_element.text = text
        new_queue_element.message_id = message_id
        new_queue_element.keyboard = pickle.dumps(reply_markup) if reply_markup else None
        new_queue_element.parse_mode = parse_mode
        new_queue_element.action = action
        new_queue_element.disable_notification = disable_notification
        new_queue_element.can_been_realized = datetime.fromtimestamp(user.delays['next_inline_keyboard_can_be_sent']
                                                                     if reply_markup
                                                                     else user.delays['next_message_can_be_sent'])
        new_queue_element.save()
        await self.calculate_user_delay(user, "message_keyboard" if reply_markup else "message")

        return True


    @staticmethod
    async def calculate_user_delay(user: UserModel, action_executed: Literal["message", "message_keyboard", "action"]):
        for delay_list in [user.delays['last_messages_sent'], user.delays['last_inline_keyboards_sent'],
                           user.delays['last_actions_executed']]:
            while (len(delay_list) > 0) and ((delay_list[0] + 60) < time()):
                delay_list.pop(0)
        if action_executed == "message":
            user.delays['last_messages_sent'].append(user.delays['next_message_can_be_sent'])
        elif action_executed == "message_keyboard":
            user.delays['last_inline_keyboards_sent'].append(user.delays['next_inline_keyboard_can_be_sent'])
        elif action_executed == "action":
            user.delays['last_actions_executed'].append(user.delays['next_action_can_be_executed'])

        total_messages_last_minute = len(user.delays['last_messages_sent'])
        total_keyboards_last_minute = len(user.delays['last_inline_keyboards_sent'])
        total_actions_last_minute = len(user.delays['last_actions_executed'])

        old_message_next_time = user.delays['next_message_can_be_sent']
        old_inline_keyboard_next_time = user.delays['next_inline_keyboard_can_be_sent']
        old_action_next_time = user.delays['next_action_can_be_executed']
        # TODO add rules for action delays

        if (total_messages_last_minute + total_keyboards_last_minute) > 55:
            user.delays['next_message_can_be_sent'] = (user.delays['last_messages_sent'][0]
                                                       if len(user.delays['last_messages_sent']) > 0 else 0) + 61
            user.delays['next_inline_keyboard_can_be_sent'] = (user.delays['last_inline_keyboards_sent'][0]
                                                               if len(user.delays['last_inline_keyboards_sent']) > 0
                                                               else 0) + 61

        if total_keyboards_last_minute > 17:
            user.delays['next_inline_keyboard_can_be_sent'] = (user.delays['last_inline_keyboards_sent'][0]
                                                               if len(user.delays['last_inline_keyboards_sent']) > 0
                                                               else 0) + 61

        if tg_api['delays']['min_message_delay'] + old_message_next_time <= user.delays['next_message_can_be_sent']:
            user.delays['next_message_can_be_sent'] = (old_message_next_time +
                                                       uniform(tg_api['delays']['min_message_delay'],
                                                               tg_api['delays']['max_message_delay']))

        if (tg_api['delays']['min_inline_keyboard_delay'] + old_inline_keyboard_next_time
                <= user.delays['next_inline_keyboard_can_be_sent']):
            user.delays['next_inline_keyboard_can_be_sent'] = (old_inline_keyboard_next_time +
                                                               uniform(tg_api['delays']['min_inline_keyboard_delay'],
                                                                       tg_api['delays']['max_inline_keyboard_delay']))

        if user.delays['next_message_can_be_sent'] <= time():
            user.delays['next_message_can_be_sent'] = (time() +
                                                       uniform(tg_api['delays']['min_message_delay'],
                                                               tg_api['delays']['max_message_delay']))

        if user.delays['next_inline_keyboard_can_be_sent'] <= time():
            user.delays['next_inline_keyboard_can_be_sent'] = (time() +
                                                               uniform(tg_api['delays']['min_inline_keyboard_delay'],
                                                                       tg_api['delays']['max_inline_keyboard_delay']))

        if user.delays['next_message_can_be_sent'] <= user.delays['last_any']:
            user.delays['next_message_can_be_sent'] = (user.delays['last_any'] +
                                                       uniform(tg_api['delays']['min_message_delay'],
                                                               tg_api['delays']['max_message_delay']))

        if user.delays['next_inline_keyboard_can_be_sent'] <= user.delays['last_any']:
            user.delays['next_inline_keyboard_can_be_sent'] = (user.delays['last_any'] +
                                                               uniform(tg_api['delays']['min_inline_keyboard_delay'],
                                                                       tg_api['delays']['max_inline_keyboard_delay']))

        user.delays['last_any'] = max(user.delays['next_message_can_be_sent'],
                                      user.delays['next_inline_keyboard_can_be_sent'],
                                      user.delays['next_action_can_be_executed'])

        user.save()


    async def sender(self):
        actions_needed = ApiQueue.objects(
            can_been_realized__lte=datetime.fromtimestamp(time())).order_by("+can_been_realized")
        for action in actions_needed:
            if self.last_message_sent + tg_api['delays']['general_delay'] < time():
                sleep(tg_api['delays']['general_delay'])
            self.last_message_sent = time()
            result = None
            try:
                if action.action == "send_message":
                    result = await self.send_message(chat_id=action.user.user_id, text=action.text,
                                                     parse_mode=action.parse_mode,
                                                     reply_markup=pickle.loads(action.keyboard)
                                                     if action.keyboard else None,
                                                     disable_notification=action.disable_notification)
                    if action.user.clear_chat and action.user.last_message:
                        await self.add_message_to_queue(action.user.user_id, action="delete_message",
                                                        message_id=action.user.last_message)
                    action.user.last_message = result.message_id
                    action.user.save()
                elif action.action == "edit_message":
                    try:
                        already = QueueCallback.objects.get(user=action.user,
                                                            message_id=str(action.message_id),
                                                            message_text=action.text,
                                                            message_inline_keyboard=action.keyboard)
                        action.delete()
                        return
                    except mongoengine.errors.DoesNotExist:
                        try:
                            already = QueueCallback.objects.get(user=action.user,
                                                                message_id=str(action.message_id))
                            result = await self.edit_message_text(chat_id=action.user.user_id, text=action.text,
                                                                  parse_mode=action.parse_mode,
                                                                  reply_markup=pickle.loads(action.keyboard)
                                                                  if action.keyboard else None,
                                                                  message_id=action.message_id)
                        except mongoengine.errors.DoesNotExist:
                            action.user.last_message = action.message_id
                            action.user.save()
                            action.delete()
                            await self.edit_message_text(chat_id=action.user.user_id,
                                                         text="This message is too old :(",
                                                         parse_mode=action.parse_mode,
                                                         message_id=action.message_id)
                            return
                elif action.action == "delete_message":
                    if action.message_id == action.user.last_message:
                        action.user.last_message = None
                        action.user.save()
                    result = await self.delete_message(chat_id=action.user.user_id, message_id=action.message_id)
                if result and (type(result) is not bool):
                    try:
                        queue_callback = QueueCallback.objects.get(user=action.user,
                                                                   message_id=str(result.message_id))
                    except mongoengine.errors.DoesNotExist:
                        queue_callback = QueueCallback()
                    queue_callback.user = action.user
                    queue_callback.key = action.callback_key if action.callback_key else str(result.message_id)
                    queue_callback.returned = pickle.dumps(result)
                    queue_callback.message_id = str(result.message_id)
                    queue_callback.message_text = action.text
                    queue_callback.message_inline_keyboard = action.keyboard
                    queue_callback.save()
                action.delete()
            except telebot.async_telebot.asyncio_helper.ApiTelegramException as e:
                if e.description in ["Forbidden: bot was blocked by the user", "Forbidden: user is deactivated"]:
                    action.user.block_bot = True
                    action.user.save()
                if re.match(r"Too Many Requests: retry after \d*", e.description):
                    self.errors_logger.warning(f"TOO MANY REQUESTS EXCEPTION; SLEEP " +
                                               re.match(r'Too Many Requests: retry after (\d*)',
                                                        e.description)[1])
                    sleep(int(re.match(r"Too Many Requests: retry after (\d*)",
                                       e.description)[1]) + 1)
                action.delete()
            except Exception as e:
                self.errors_logger.error(f"""ERROR EXCEPTED: {e} tb: {traceback.format_exc()}""")



    async def check_rules(self, message: telebot.types.Message = None, callback: telebot.types.CallbackQuery = None):
        user_id = message.chat.id if message else callback.from_user.id
        user_dict = message.from_user if message else callback.from_user

        try:
            user = UserModel.objects.get(user_id=user_id)
        except mongoengine.errors.DoesNotExist:
            user = UserModel(user_id = user_dict.id, f_n=getattr(user_dict, "first_name", None),
                             l_n=getattr(user_dict, "last_name", None),
                             acc_name=getattr(user_dict, "username", None))
            user.save()
        if user.banned:
            return False

        current_queue = ApiQueue.objects(user=user).count()

        if current_queue >= bot_config['max_actions_per_user']:
            user.spam_alert += 1
            user.save()
            return False

        # TODO add ban function

        if getattr(user_dict, "first_name", None) != user.f_n:
            user.f_n = getattr(user_dict, "first_name", None)
        if getattr(user_dict, "last_name", None) != user.l_n:
            user.l_n = getattr(user_dict, "last_name", None)
        if getattr(user_dict, "username", None) != user.acc_name:
            user.acc_name = getattr(user_dict, "username", None)

        if user.block_bot:
            user.block_bot = False
        user.save()

        if user.user_id in bot_config['admins_ids']:
            return True

        if (time() - self.start_time) < 5:
            return False

        if user.banned:
            return False

        return True
