import vk_api, random
import sqlite3
import os

from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = os.environ.get('BOT_TOKEN')
vk_session = vk_api.VkApi(token = TOKEN)

longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

conn = sqlite3.connect("db.db")
c = conn.cursor()

global Random


def random_id():
    Random = 0
    Random += random.randint(0, 1000000000);
    return Random


def check_if_exists(user_id):
    c.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True


def register_new_user(user_id):
    c.execute("INSERT INTO users(user_id, state) VALUES (%d, '')" % user_id)
    conn.commit()
    c.execute("INSERT INTO user_info(user_id, user_wish) VALUES (%d, 0)" % user_id)
    conn.commit()


def get_user_state(user_id):
    c.execute("SELECT state FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


def get_user_wish(user_id):
    c.execute("SELECT user_wish FROM user_info WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


def set_user_wish(user_id, user_wish):
    c.execute("UPDATE user_info SET user_wish = %d WHERE user_id = %d" % (user_wish, user_id))
    conn.commit()


while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            if not check_if_exists(event.user_id):
                register_new_user(event.user_id)

            if event.text.lower() == "начать":
                vk.messages.send(
                    user_id=event.user_id,
                    message="Приветик!\nЯ бот Лёха говна лепёха.\nМогу я Вам чем-то помочь?",
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )

            elif event.text.lower() == "🎯 сайт":
                if get_user_wish(event.user_id) == 1:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="🎯 Наш сайт: https://modshanshop.ru",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id()
                    )
            elif event.text.lower() == "🌚 о нас":
                if get_user_wish(event.user_id) == 1:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="🌚 Мы команда хакеров которые могут взломать любой пиратский сервер майнкрафт без смс и регистрации.\nВы можете присылать нам IP адреса серверов которые обманывают на команды или донат",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id()
                    )
            elif event.text.lower() == "🌏 правила":
                if get_user_wish(event.user_id) == 1:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="🌏 Правила пользования: https://vk.com/topic-183789286_39359574",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id()
                    )

            else:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Неизвестная команда",
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )
