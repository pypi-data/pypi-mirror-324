from mongoengine import *


class UserModel(Document):
    meta = {"collection": "users"}
    user_id = IntField(required=True, unique=True)
    acc_name = StringField()
    f_n = StringField()
    l_n = StringField()
    spam_alert = IntField()
    banned = BooleanField(default=False)
    last_message = IntField()
    clear_chat = BooleanField(default=False)
    ban_ends = DateTimeField()
    block_bot = BooleanField(default=False)
    delays = DictField(default={
        "last_messages_sent": [],
        "last_inline_keyboards_sent": [],
        "last_actions_executed": [],
        "next_message_can_be_sent": 0,
        "next_inline_keyboard_can_be_sent": 0,
        "next_action_can_be_executed": 0,
        "last_any": 0
    })
