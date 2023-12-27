import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload
import sqlite3
import random
import requests


vk_session = vk_api.VkApi(token='vk1.a.bxYN9Vw1qFlrtSMiNhNaULcqbTjlCroxhGBlDglZaLibdgdxp5ETUEVbRiHpB-B8dOEIlh1VFzpX3FTjTKEhNH7sg7qUxa6O3RUXeogyL-1Pf4-kFeiLqFyRgiXsR59DLMLUgxSMLaHIYv8lZ-SxTPI7bYq-59ZoWmXu0J05WgCQp6hsbbdAmz-mCJQk4sjqcTOezqRAVm9SvbOcD1VQMA')
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 221894301)



# подключение к базе данных
con = sqlite3.connect('database.db', check_same_thread=False)
cursor = con.cursor()

# cursor.execute("""DROP TABLE profiles""")
# cursor.execute("""CREATE TABLE profiles (id integer, age integer, gender text, city text, name text, text text, photo text)""")
# con.commit()
# # quit()
#
# cursor.execute("""DROP TABLE owner""")
# cursor.execute("""DROP TABLE admins""")
#
# cursor.execute("""CREATE TABLE owner (id integer)""")
# cursor.execute("""INSERT INTO owner VALUES (238340436)""")
#
# cursor.execute("""CREATE TABLE admins (id integer)""")
# cursor.execute("""INSERT INTO admins VALUES (238340436)""")
# # cursor.execute("""DELETE FROM admins WHERE id = 238340436""")
# con.commit()
# quit()


razdel = []

queue, stage, date = [], [], []

id_change, date_change = [], []

id_searching, id_searched = [], []

like_for, like_from = [], []

id_who_search, param_search = [], []

settings_chat, queue_chat = [], []
chat_one, name_one, chat_two, name_two = [], [], [], []

settings_anon = []
queue_anon_chat, anon_chat_one, anon_chat_two = [], [], []

likes = []
queue_likes, count_likes = [], []

def slsldlsl():
    global razdel
    global queue
    global stage
    global date
    global id_change
    global date_change
    global id_searching
    global id_searched
    global like_for
    global like_from
    global id_who_search
    global param_search
    global settings_chat
    global queue_chat
    global chat_one
    global chat_two
    global name_two
    global name_one
    global settings_anon
    global queue_anon_chat
    global anon_chat_one
    global anon_chat_two
    global likes
    global queue_likes
    global count_likes

slsldlsl()
####################################################################################################

def get_owner(id=-1):
    if id == -1:
        cursor.execute("""SELECT * FROM owner""")
        return cursor.fetchall()[0][0]
    else:
        set_admin(get_owner(), id)
        cursor.execute(f"""UPDATE owner SET id = {str(id)}""")
        con.commit()
        return 'Владелец изменен.'

def get_admins(id):
    cursor.execute("""SELECT * FROM admins""")
    admins = []
    cur_admins = cursor.fetchall()
    for i in cur_admins:
        admins.append(i[0])
    return admins

def set_admin(from_id, id):
    # try:
        if from_id == get_owner():
            admins = get_admins(from_id)
            if id in admins:
                return 'Этот пользователь и так админ.'
            else:
                cursor.execute(f"""INSERT INTO admins VALUES ({str(id)})""")
                con.commit()
                return 'Админ назначен.'
        else:
            return False
    # except:
    #     return False

def del_admin(from_id, id):
    try:
        if from_id == get_owner():
            admins = get_admins(from_id)
            if id in admins:
                cursor.execute(f"""DELETE FROM admins WHERE id = {str(id)}""")
                con.commit()
                return 'Админ удален.'
            else:
                return 'Пользователь не является админом.'
        else:
            return False
    except:
        return False

def sending_all(id, msg):
    offset = 0
    go = True
    users = []
    while go:
        vskk = vk.messages.getConversations(count=200, offset=offset)['items']
        for i in vskk:
            users.append(int(i['conversation']['peer']['id']))
        if len(vskk)<200:
            go = False
    for i in users:
        try:
            send_message(i, msg)
        except:
            users.remove(i)
    return f'Отправлено {str(len(users))} пользователям!'

def set_razdel(id, razd):
    if len(razdel) == 0:
        razdel.append({'id': id, 'razdel': razd})
        return razd
    else:
        for i in razdel:
            if i['id'] == int(id):
                i['razdel'] = razd
                return razd
        razdel.append({'id': id, 'razdel': razd})
        return razd

def get_razdel(id):
    if len(razdel) == 0:
        set_razdel(id, 'general')
        return 'general'
    else:
        for i in razdel:
            if i['id'] == int(id):
                return i['razdel']
        set_razdel(id, 'general')
        return 'general'



def get_kb(razd):
    kb = VkKeyboard()
    if razd == 'general':
        kb.add_button('Перейти к анкетам', VkKeyboardColor.POSITIVE)
        kb.add_button('Найти чат', VkKeyboardColor.PRIMARY)
        kb.add_button('Найти анонимный чат', VkKeyboardColor.PRIMARY)
        kb.add_button('Моя анкета', VkKeyboardColor.NEGATIVE)
    elif razd == 'anon_chat':
        # kb = VkKeyboard()
        kb.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    elif razd == 'set_anon_1':
        kb.add_button('Мужской', VkKeyboardColor.PRIMARY)
        kb.add_button('Женский', VkKeyboardColor.NEGATIVE)
        kb.add_line()
        kb.add_button('Неважно', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'set_anon_2':
        kb.add_button('0-17', VkKeyboardColor.SECONDARY)
        kb.add_button('18-29', VkKeyboardColor.SECONDARY)
        kb.add_button('30+', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Неважно', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'set_anon_3':
        kb.add_button('Неважно', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'wait_anon':
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'open_chat':
        # kb = VkKeyboard()
        kb.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    elif razd == 'set_open_1':
        kb.add_button('Мужской', VkKeyboardColor.PRIMARY)
        kb.add_button('Женский', VkKeyboardColor.NEGATIVE)
        kb.add_line()
        kb.add_button('Неважно', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'set_open_2':
        kb.add_button('0-17', VkKeyboardColor.SECONDARY)
        kb.add_button('18-29', VkKeyboardColor.SECONDARY)
        kb.add_button('30+', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Неважно', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'set_open_3':
        kb.add_button('Неважно', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'wait_open':
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'set_search_1':
        kb.add_button('Мужской', VkKeyboardColor.PRIMARY)
        kb.add_button('Женский', VkKeyboardColor.NEGATIVE)
        kb.add_line()
        kb.add_button('Неважно', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'set_search_2':
        kb.add_button('0-17', VkKeyboardColor.SECONDARY)
        kb.add_button('18-29', VkKeyboardColor.SECONDARY)
        kb.add_button('30+', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Неважно', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'set_search_3':
        kb.add_button('Неважно', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'searching':
        kb.add_button('👍', VkKeyboardColor.POSITIVE)
        kb.add_button('👎', VkKeyboardColor.POSITIVE)
        kb.add_button('💌', VkKeyboardColor.NEGATIVE)
        kb.add_button('💤', VkKeyboardColor.SECONDARY)
    elif razd == 'send_like':
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'show_like':
        kb.add_button('👍', VkKeyboardColor.POSITIVE)
        kb.add_button('👎', VkKeyboardColor.NEGATIVE)
    elif razd == 'check_like':
        kb.add_button('Показать', VkKeyboardColor.POSITIVE)
    elif razd == 'my_anketa':
        kb.add_button('Перейти к анкетам', VkKeyboardColor.POSITIVE)
        kb.add_line()
        kb.add_button('Изменить имя', VkKeyboardColor.SECONDARY)
        kb.add_button('Изменить возраст', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Изменить город', VkKeyboardColor.SECONDARY)
        kb.add_button('Изменить текст', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Изменить фото', VkKeyboardColor.SECONDARY)
        kb.add_button('Удалить анкету', VkKeyboardColor.NEGATIVE)
        kb.add_line()
        kb.add_button('Главное меню', VkKeyboardColor.PRIMARY)
    elif razd == 'create_main':
        kb.add_button('Создать анкету', VkKeyboardColor.POSITIVE)
        kb.add_line()
        kb.add_button('Вернуться', VkKeyboardColor.SECONDARY)
    elif razd == 'create_1':
        kb.add_button('Мужской', VkKeyboardColor.PRIMARY)
        kb.add_button('Женский', VkKeyboardColor.NEGATIVE)
    elif razd == 'create_5':
        kb.add_button('Не указывать текст', VkKeyboardColor.NEGATIVE)
    elif razd == 'change_name' or razd == 'change_age' or razd == 'change_city' or razd == 'change_photo':
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    elif razd == 'change_text':
        kb.add_button('Не указывать текст', VkKeyboardColor.SECONDARY)
        kb.add_line()
        kb.add_button('Отменить', VkKeyboardColor.NEGATIVE)
    return kb.get_keyboard()

def get_help(razd):
    if razd == 'general':
        return '1. Перейти к анкетам 💞\n2. Найти чат 👻\n3. Найти анонимный чат 😈\n4. Моя анкета 💦'
    elif razd == 'create_main':
        return '1. Создать анкету'
    elif razd == 'my_anketa':
        return '1. Перейти к анкетам\n\n2. Изменить имя\n3. Изменить возраст\n4. Изменить город\n5. Изменить текст\n6. Изменить фото\n\n7. Удалить анкету\n8. Главное меню'


def check_profile(id):
    cursor.execute("""SELECT * FROM profiles""")
    profiles = cursor.fetchall()
    for i in profiles:
        if i[0] == id:
            return True
    return False

def add_profile(id, age, gender, city, name, text, photo):
    cursor.execute(f"""INSERT INTO profiles VALUES ({str(id)}, {str(age)}, '{gender}', '{city}', '{name}', '{text}', '{photo}')""")
    con.commit()

def get_profile(id):
    cursor.execute("""SELECT * FROM profiles""")
    profiles = cursor.fetchall()
    msg, photo = '', ''
    for i in profiles:
        if i[0] == id:
            msg, photo = f'{i[4]}, {i[1]}, {i[3]}\n\n{i[5]}', i[6]
            break
    return msg, photo

def change_profile(id, what, to, attachments):
    if what=='photo':
        height, url = 0, ''
        if len(attachments) > 0:
            if attachments[0]['type'] == 'photo':
                for i in attachments[0]['photo']['sizes']:
                    if i['height'] > height:
                        height, url = i['height'], i['url']

                img = requests.get(url).content
                with open(f'photos/{str(id)}.png', 'wb') as f:
                    f.write(img)
                upload = VkUpload(vk)
                owner, photo, key = upload_photo(upload, f'photos/{str(id)}.png')
                cursor.execute(f"""UPDATE profiles SET {what} = 'photo{str(owner)}_{str(photo)}_{str(key)}' WHERE id = {str(id)}""")
                con.commit()
                set_razdel(id, 'general')
                return True
            else:
                return 'Нет, пришли мне одну фотографию. И не файлом.'
        else:
            return 'Нет, пришли мне одну фотографию. И не файлом.'
    else:
        if what == 'age':
            try:
                int(to)
                cursor.execute(f"""UPDATE profiles SET {what} = {str(to)} WHERE id = {str(id)}""")
                con.commit()
                set_razdel(id, 'general')
                return True
            except:
                return 'Напиши цифрами.'
        else:
            cursor.execute(f"""UPDATE profiles SET {what} = '{to}' WHERE id = {str(id)}""")
            con.commit()
            set_razdel(id, 'general')
            return True

def del_profile(id):
    if check_profile(id):
        cursor.execute(f"""DELETE FROM profiles WHERE id = {str(id)}""")
        con.commit()
        return 'Анкета удалена.\n\nЧтобы создать новую, напишите "начать"'
    else:
        return 'У вас нет анкеты.\n\nЧтобы создать, напишите "начать"'

def search(id, age=None, gender=None, city=None):
    cursor.execute("""SELECT * FROM profiles""")
    profiles = cursor.fetchall()
    searching = []
    for i in profiles:
        if age == None and gender == None and city == None:
            if int(i[0]) != int(id):
                searching.append(i)
        elif age != None and gender != None and city == None:
            if age == '0-17':
                if int(i[0]) != int(id) and i[1] <= 17 and i[2] == gender:
                    searching.append(i)
            elif age == '18-29':
                if int(i[0]) != int(id) and 18 <= i[1] <= 29 and i[2] == gender:
                    searching.append(i)
            elif age == '30+':
                if int(i[0]) != int(id) and i[1] >= 30 and i[2] == gender:
                    searching.append(i)
            else:
                if int(i[0]) != int(id) and i[1] == age and i[2] == gender:
                    searching.append(i)
        elif age != None and gender != None and city != None:
            if age == '0-17':
                if int(i[0]) != int(id) and i[1] <= 17 and i[2] == gender and i[3] == city:
                    searching.append(i)
            elif age == '18-29':
                if int(i[0]) != int(id) and 18 <= i[1] <= 29 and i[2] == gender and i[3] == city:
                    searching.append(i)
            elif age == '30+':
                if int(i[0]) != int(id) and i[1] >= 30 and i[2] == gender and i[3] == city:
                    searching.append(i)
            else:
                if int(i[0]) != int(id) and i[1] == age and i[2] == gender and i[3] == city:
                    searching.append(i)
        elif age == None and gender != None and city == None:
            if int(i[0]) != int(id) and i[2] == gender:
                searching.append(i)
        elif age == None and gender != None and city != None:
            if int(i[0]) != int(id) and i[2] == gender and i[3] == city:
                searching.append(i)
        elif age != None and gender == None and city != None:
            if age == '0-17':
                if int(i[0]) != int(id) and i[1] <= 17 and i[3] == city:
                    searching.append(i)
            elif age == '18-29':
                if int(i[0]) != int(id) and 18 <= i[1] <= 29 and i[3] == city:
                    searching.append(i)
            elif age == '30+':
                if int(i[0]) != int(id) and i[1] >= 30 and i[3] == city:
                    searching.append(i)
            else:
                if int(i[0]) != int(id) and i[1] == age and i[3] == city:
                    searching.append(i)
        elif age == None and gender == None and city != None:
            if int(i[0]) != int(id) and i[3] == city:
                searching.append(i)
        elif age != None and gender == None and city == None:
            if age == '0-17':
                if int(i[0]) != int(id) and i[1] <= 17:
                    searching.append(i)
            elif age == '18-29':
                if int(i[0]) != int(id) and 18 <= i[1] <= 29:
                    searching.append(i)
            elif age == '30+':
                if int(i[0]) != int(id) and i[1] >= 30:
                    searching.append(i)
            else:
                if int(i[0]) != int(id) and i[1] == age:
                    searching.append(i)
    if len(searching) > 0:
        user = random.choice(searching)
        msg, photo = get_profile(user[0])
        try:
            ind = id_searching.index(id)
            id_searching[ind] = id
            id_searched[ind] = user[0]
        except:
            id_searched.append(user[0]); id_searching.append(id)
        send_message(id, msg, get_kb('searching'), attachment=photo)
    else:
        param_search.remove(param_search[id_who_search.index(id)])
        id_who_search.remove(id)
        set_razdel(id, 'general')
        send_message(id, 'К сожалению, анкет по запросу не найдено 🥺\nПопробуй вписать новые параметры.\n\n'+get_help('general'))
        if id in queue_likes:
            set_razdel(id, 'check_like')
            send_message(id,
                         f'Тебя лайкнули {str(count_likes[queue_likes.index(id)])} пользователей!\n\n1. Показать',
                         get_kb('check_like'))
            count_likes.remove(count_likes[queue_likes.index(id)])
            queue_likes.remove(id)



def show_like(id, status):
    local = []
    if status == 'like':
        from_id = like_from[like_for.index(id)]
        msg, photo = get_profile(from_id)
        send_message(from_id, f'Есть взаимная симпатия - vk.com/id{str(id)}\n\n{msg}', attachment=photo)
        send_message(id, f'Отлично! Приятного общения ~ vk.com/id{str(from_id)}')
        like_from.remove(from_id); like_for.remove(id)
        delete_like(id, from_id)
        show_like(id, 'show')
    elif status == 'dis':
        from_id = like_from[like_for.index(id)]
        like_from.remove(from_id); like_for.remove(id)
        delete_like(id, from_id)
        show_like(id, 'show')
    elif status == 'show':
        for i in likes:
            if i['for_id'] == id:
                like_for.append(id); like_from.append(i['from_id'][0])
                msg, photo = get_profile(i['from_id'][0])
                set_razdel(id, 'show_like')
                if i['from_message'][0] is not None and i['from_message'][0] != 'None' and len(i['from_message'][0])>0:
                    send_message(id, f'{msg}\n\nСообщение для тебя:\n{i["from_message"][0]}', keyboard=get_kb('show_like'), attachment=photo)
                else:
                    send_message(id, f'{msg}', keyboard=get_kb('show_like'), attachment=photo)



def like(from_id, message=None, send=False):
    if send:
        set_razdel(from_id, 'send_like')
        send_message(from_id, 'Теперь напиши сообщение для этого человека.\n\n1. Отменить', keyboard=get_kb('send_like'))
    else:
        if check_like(from_id):
            pass
        else:
            for_id = id_searched[id_searching.index(from_id)]
            count = 0
            tr = False
            if len(likes)==0:
                likes.append({'for_id': int(for_id), 'from_id': [int(from_id)], 'from_message': [message]})
                count = 1
            else:
                for i in likes:
                    if i['for_id'] == for_id:
                        tr = True
                        i['from_id'].append(int(from_id)); i['from_message'].append(message)
                        count = len(i['from_id'])
                if tr == False:
                    likes.append({'for_id': int(for_id), 'from_id': [int(from_id)], 'from_message': [message]})
                    count = 1
            if get_razdel(for_id) == 'open_chat' or get_razdel(for_id) == 'set_open_1' or get_razdel(for_id) == 'set_open_2' or get_razdel(for_id) == 'set_open_3' or get_razdel(for_id) == 'wait_open' or get_razdel(for_id) == 'anon_chat' or get_razdel(for_id) == 'wait_anon' or get_razdel(for_id) == 'set_anon_1' or get_razdel(for_id) == 'set_anon_2' or get_razdel(for_id) == 'set_anon_3' or get_razdel(for_id) == 'searching' or get_razdel(for_id) == 'set_search_1' or get_razdel(for_id) == 'set_search_2' or get_razdel(for_id) == 'set_search_3':
                if for_id in queue_likes:
                    count_likes[queue_likes.index(for_id)] = count
                else:
                    queue_likes.append(for_id); count_likes.append(count)
            else:
                set_razdel(for_id, 'check_like')
                send_message(for_id, f'Тебя лайкнули {str(count)} пользователей!\n\n1. Показать', get_kb('check_like'))
            return likes

def check_like(from_id):
    for i in likes:
        if from_id in i['from_id']:
            return True
    return False

def delete_like(for_id, from_id):
    if len(likes)==0:
        pass
    else:
        for i in likes:
            if i['for_id'] == for_id:
                if len(i['from_id'])>1:
                    i['from_message'].remove(i['from_message'][i['from_id'].index(from_id)]); i['from_id'].remove(from_id)
                else:
                    likes.remove(i)
                    set_razdel(for_id, 'general')
                    send_message(for_id, f'На этом всё.\n\n{get_help("general")}', keyboard=get_kb('general'))
    return likes

####################################################################################################

def create_profile(id, arg):
    ind = queue.index(id)
    if stage[ind] == 'gender':
        if arg.lower() == 'мужской' or arg.lower() == 'женский':
            date[ind] = {'id': id, 'age': date[ind]['age'], 'gender': arg, 'city': date[ind]['city'], 'name': date[ind]['name'], 'text': date[ind]['text'], 'photo': date[ind]['photo']}
            stage[ind] = 'name'
            set_razdel(id, 'create_2')
            return 'Как тебя зовут?'
        else:
            send_message(id, 'Выбери нужный вариант ответа.\n\n1. Мужской\n2. Женский')
    elif stage[ind] == 'name':
        date[ind] = {'id': id, 'age': date[ind]['age'], 'gender': date[ind]['gender'], 'city': date[ind]['city'], 'name': arg, 'text': date[ind]['text'], 'photo': date[ind]['photo']}
        stage[ind] = 'age'
        set_razdel(id, 'create_3')
        return 'Сколько тебе лет?'
    elif stage[ind] == 'age':
        try:
            int(arg)
            date[ind] = {'id': id, 'age': arg, 'gender': date[ind]['gender'], 'city': date[ind]['city'], 'name': date[ind]['name'], 'text': date[ind]['text'], 'photo': date[ind]['photo']}
            stage[ind] = 'city'
            set_razdel(id, 'create_4')
            return 'Напиши свой город.'
        except:
            return 'Напиши цифрами.'
    elif stage[ind] == 'city':
        date[ind] = {'id': id, 'age': date[ind]['age'], 'gender': date[ind]['gender'], 'city': arg, 'name': date[ind]['name'], 'text': date[ind]['text'], 'photo': date[ind]['photo']}
        stage[ind] = 'text'
        set_razdel(id, 'create_5')
        return 'Расскажи о себе. Этот текст будут видеть другие пользователи при поиске.\n\n1. Не указывать текст'
    elif stage[ind] == 'text':
        if arg.lower() == 'не указывать текст' or arg == '1':
            arg = ''
        date[ind] = {'id': id, 'age': date[ind]['age'], 'gender': date[ind]['gender'], 'city': date[ind]['city'], 'name': date[ind]['name'], 'text': arg, 'photo': date[ind]['photo']}
        stage[ind] = 'photo'
        set_razdel(id, 'create_6')
        return 'Теперь пришли мне одну фотографию, которая будет у тебя в анкете.'
    elif stage[ind] == 'photo':
        try:
            attachments, height, url = arg.obj.message['attachments'], 0, ''
            if len(attachments) > 0:
                if attachments[0]['type'] == 'photo':
                    for i in attachments[0]['photo']['sizes']:
                        if i['height'] > height:
                            height, url = i['height'], i['url']

                    img = requests.get(url).content
                    with open(f'photos/{str(id)}.png', 'wb') as f:
                        f.write(img)
                    upload = VkUpload(vk)
                    owner, photo, key = upload_photo(upload, f'photos/{str(id)}.png')

                    date[ind] = {'id': id, 'age': date[ind]['age'], 'gender': date[ind]['gender'], 'city': date[ind]['city'], 'name': date[ind]['name'], 'text': date[ind]['text'], 'photo': f'photo{str(owner)}_{str(photo)}_{str(key)}'}
                    add_profile(date[ind]['id'], date[ind]['age'], date[ind]['gender'], date[ind]['city'], date[ind]['name'], date[ind]['text'], date[ind]['photo'])
                    queue.remove(queue[ind])
                    stage.remove(stage[ind])
                    date.remove(date[ind])
                    set_razdel(id, 'general')
                    return 'Анкета добавлена! 🥳\n\n'+get_help('general')
                else:
                    return 'Нет, пришли мне одну фотографию. И не файлом.'
            else:
                return 'Нет, пришли мне одну фотографию. И не файлом.'
        except:
            return 'Нет, пришли мне одну фотографию. И не файлом.'


def set_search(id, arg):
    ind = id_who_search.index(id)
    if arg.lower() == 'отменить':
        param_search.remove(param_search[ind]); id_who_search.remove(id)
        set_razdel(id, 'general')
        send_message(id, 'Поиск отменен.\n\n'+get_help('general'), get_kb('general'))
    else:
        if arg == 'Неважно':
            arg = None
        if param_search[ind]['gender'] == '':
            if arg == None or arg.lower() == 'мужской' or arg.lower() == 'женский':
                param_search[ind] = {'gender': arg, 'age': param_search[ind]['age'], 'city': param_search[ind]['city'], 'done': False}
                set_razdel(id, 'set_search_2')
                send_message(id, 'Какой возраст тебя интересует?\n\n1. 0-17\n2. 18-29\n3. 30+\n4. Неважно\n\n5. Отменить', get_kb('set_search_2'))
            else:
                send_message(id, 'Выбери правильный вариант ответа.\n\n1. Мужской\n2. Женский\n3. Неважно\n\n4. Отменить', get_kb('set_search_1'))
        elif param_search[ind]['gender'] != '' and param_search[ind]['age'] == '':
            try:
                if arg == '0-17' or arg == '18-29' or arg == '30+':
                    pass
                else:
                    int(arg)
                param_search[ind] = {'gender': param_search[ind]['gender'], 'age': arg, 'city': param_search[ind]['city'], 'done': False}
                set_razdel(id, 'set_search_3')
                send_message(id, 'В каком городе ищем?\n\n1. Неважно\n2. Отменить', get_kb('set_search_3'))
            except:
                if arg == None:
                    param_search[ind] = {'gender': param_search[ind]['gender'], 'age': arg,
                                         'city': param_search[ind]['city'], 'done': False}
                    set_razdel(id, 'set_search_3')
                    send_message(id, 'В каком городе ищем?\n\n1. Неважно\n2.Отменить', get_kb('set_search_3'))
                else:
                    send_message(id, 'Напиши цифрами.\n\n1. 0-17\n2. 18-29\n3. 30+\n4. Неважно\n\n5. Отменить', get_kb('set_search_2'))
        elif param_search[ind]['age'] != '' and param_search[ind]['city'] == '':
            param_search[ind] = {'gender': param_search[ind]['gender'], 'age': param_search[ind]['age'], 'city': arg, 'done': True}
            set_razdel(id, 'searching')
            send_message(id, '👇')
            search(id, param_search[ind]['age'], param_search[ind]['gender'], param_search[ind]['city'])

def check_anon(id):
    for i in settings_anon:
        if i['id'] == id:
            return True
    return False

def set_anon(id, arg):
    razd = get_razdel(id)
    iss = True
    if arg == 'отменить':
        for i in settings_anon:
            if i['id'] == id:
                iss = False
                if id in queue_anon_chat:
                    queue_anon_chat.remove(id)
                settings_anon.remove(i)
                set_razdel(id, 'general')
                send_message(id, 'Отменили!\n\n'+get_help('general'), get_kb('general'))
        if iss:
            if id in queue_anon_chat:
                queue_anon_chat.remove(id)
            set_razdel(id, 'general')
            send_message(id, f'Отменили!\n\n{get_help("general")}', get_kb('general'))
        if id in queue_likes:
            set_razdel(id, 'check_like')
            send_message(id, f'Тебя лайкнули {str(count_likes[queue_likes.index(id)])} пользователей!\n\n1. Показать', get_kb('check_like'))
            count_likes.remove(count_likes[queue_likes.index(id)])
            queue_likes.remove(id)
    else:
        if arg.lower() == 'неважно':
            arg = None
        if check_anon(id):
            for i in settings_anon:
                if i['id'] == id:
                    if razd == 'set_anon_2':
                        i['age'] = arg
                        set_razdel(id, 'set_anon_3')
                        return 'Теперь укажи город, в котором будем искать чат.\n\n1. Неважно\n2. Отменить'
                    elif razd == 'set_anon_3':
                        if arg != None:
                            arg = arg.lower()
                        i['city'] = arg
                        i['search'] = True
                        set_razdel(id, 'wait_anon')
                        return 'Поиск собеседника 🧸\n\n1. Отменить'
        else:
            settings_anon.append({'id': id, 'gender': arg, 'age': None, 'city': None, 'search': False})
            queue_anon_chat.append(id)
            set_razdel(id, 'set_anon_2')
            return 'Теперь укажи возраст, по которому будем искать чат.\n\n1. 0-17\n2. 18-29\n3. 30+\n4. Неважно\n\n5. Отменить'


def start_anon(id, age=None, gender=None, city=None):
    if len(queue_anon_chat)>1:
        searching = []
        one = []
        for i in settings_anon:
            if int(i['id']) == int(id):
                one.append(i)
            else:
                if i['search']:
                    if age == None and gender == None and city == None:
                        if int(i['id']) != int(id):
                            searching.append(i)
                    elif age != None and gender != None and city == None:
                        if int(i['id']) != int(id) and i['age'] == age and i['gender'] != gender:
                            searching.append(i)
                    elif age != None and gender != None and city != None:
                        if int(i['id']) != int(id) and i['age'] == age and i['gender'] != gender and i['city'] == city:
                            searching.append(i)
                    elif age == None and gender != None and city == None:
                        if int(i['id']) != int(id) and i['gender'] != gender:
                            searching.append(i)
                    elif age == None and gender != None and city != None:
                        if int(i['id']) != int(id) and i['gender'] != gender and i['city'] == city:
                            searching.append(i)
                    elif age != None and gender == None and city != None:
                        if int(i['id']) != int(id) and i['age'] == age and i['city'] == city:
                            searching.append(i)
                    elif age == None and gender == None and city != None:
                        if int(i['id']) != int(id) and i['city'] == city:
                            searching.append(i)
        if len(searching) > 0:
            two_id = random.choice(searching)
            anon_chat_one.append(two_id['id'])
            anon_chat_two.append(id)
            queue_anon_chat.remove(two_id['id']); settings_anon.remove(one[0])
            queue_anon_chat.remove(id); settings_anon.remove(two_id)
            set_razdel(id, 'anon_chat')
            set_razdel(two_id['id'], 'anon_chat')
            send_message(two_id['id'], 'Собеседник найден, приятного общения!\n\nЧтобы завершить диалог, нажми на кнопку снизу.',
                         keyboard=get_kb('anon_chat'))
            send_message(id, 'Собеседник найден, приятного общения!\n\nЧтобы завершить диалог, нажми на кнопку снизу.',
                         keyboard=get_kb('anon_chat'))

def stop_anon(one_id, two_id):
    if one_id in queue_anon_chat:
        settings_anon.remove(settings_anon[queue_anon_chat.index(one_id)])
        queue_anon_chat.remove(one_id)
        set_razdel(one_id, 'general')
        send_message(one_id, 'Поиск завершен\n\n'+get_help('general'), get_kb('general'))
        if one_id in queue_likes:
            set_razdel(one_id, 'check_like')
            send_message(one_id, f'Тебя лайкнули {str(count_likes[queue_likes.index(one_id)])} пользователей!\n\n1. Показать', get_kb('check_like'))
            count_likes.remove(count_likes[queue_likes.index(one_id)])
            queue_likes.remove(one_id)
    else:
        if one_id in anon_chat_one:
            anon_chat_one.remove(one_id); anon_chat_two.remove(two_id)
        elif one_id in anon_chat_two:
            anon_chat_one.remove(two_id); anon_chat_two.remove(one_id)
        if one_id in queue_likes:
            set_razdel(one_id, 'check_like')
            send_message(one_id, f'Тебя лайкнули {str(count_likes[queue_likes.index(one_id)])} пользователей!\n\n1. Показать', get_kb('check_like'))
            count_likes.remove(count_likes[queue_likes.index(one_id)])
            queue_likes.remove(one_id)
        else:
            set_razdel(one_id, 'general')
            send_message(one_id, 'Диалог завершен.\n\n'+get_help('general'), keyboard=get_kb('general'))
        if two_id in queue_likes:
            set_razdel(two_id, 'check_like')
            send_message(two_id, f'Тебя лайкнули {str(count_likes[queue_likes.index(two_id)])} пользователей!\n\n1. Показать', get_kb('check_like'))
            count_likes.remove(count_likes[queue_likes.index(two_id)])
            queue_likes.remove(two_id)
        else:
            set_razdel(two_id, 'general')
            send_message(two_id, 'Собеседник завершил диалог.\n\n'+get_help('general'), keyboard=get_kb('general'))

def anon_chat(id, msg):
    if id in anon_chat_one:
        if len(msg)>0:
            two = anon_chat_two[anon_chat_one.index(id)]
            if msg.lower() == 'завершить':
                stop_anon(id, two)
            else:
                send_message(two, msg, keyboard=get_kb('anon_chat'))
    elif id in anon_chat_two:
        if len(msg)>0:
            two = anon_chat_one[anon_chat_two.index(id)]
            if msg.lower() == 'завершить':
                stop_anon(id, two)
            else:
                send_message(two, msg, keyboard=get_kb('anon_chat'))
    else:
        send_message(id, 'Произошла ошибка.')
        set_razdel(id, 'general')
        send_message(id, get_help('general'), keyboard=get_kb('general'))



def check_open(id):
    for i in settings_chat:
        if i['id'] == id:
            return True
    return False

def set_open(id, arg):
    razd = get_razdel(id)
    iss = True
    if arg == 'отменить':
        for i in settings_chat:
            if i['id'] == id:
                iss = False
                if id in queue_chat:
                    queue_chat.remove(id)
                settings_chat.remove(i)
                set_razdel(id, 'general')
                send_message(id, f'Отменили!\n\n{get_help("general")}', get_kb('general'))
        if iss:
            if id in queue_chat:
                queue_chat.remove(id)
            set_razdel(id, 'general')
            send_message(id, f'Отменили!\n\n{get_help("general")}', get_kb('general'))
        if id in queue_likes:
            set_razdel(id, 'check_like')
            send_message(id, f'Тебя лайкнули {str(count_likes[queue_likes.index(id)])} пользователей!\n\n1. Показать', get_kb('check_like'))
            count_likes.remove(count_likes[queue_likes.index(id)])
            queue_likes.remove(id)
        return 1
    else:
        if arg.lower() == 'неважно':
            arg = None
        if check_open(id):
            for i in settings_chat:
                if i['id'] == id:
                    if razd == 'set_open_2':
                        i['age'] = arg
                        set_razdel(id, 'set_open_3')
                        return 'Теперь укажи город, в котором будем искать чат.\n\n1. Неважно\n2. Отменить'
                    elif razd == 'set_open_3':
                        if arg != None:
                            arg = arg.lower()
                        i['city'] = arg
                        i['search'] = True
                        set_razdel(id, 'wait_open')
                        return 'Поиск собеседника 🧸\n\n1. Отменить'
        else:
            settings_chat.append({'id': id, 'gender': arg, 'age': None, 'city': None, 'search': False})
            queue_chat.append(id)
            set_razdel(id, 'set_open_2')
            return 'Теперь укажи возраст, по которому будем искать чат.\n\n1. 0-17\n2. 18-29\n3. 30+\n4. Неважно\n\n5. Отменить'


def start_open(id, age=None, gender=None, city=None):
    if len(queue_chat)>1:
        searching = []
        one = []
        for i in settings_chat:
            if int(i['id']) == int(id):
                one.append(i)
            else:
                if i['search']:
                    if age == None and gender == None and city == None:
                        if int(i['id']) != int(id):
                            searching.append(i)
                    elif age != None and gender != None and city == None:
                        if int(i['id']) != int(id) and i['age'] == age and i['gender'] != gender:
                            searching.append(i)
                    elif age != None and gender != None and city != None:
                        if int(i['id']) != int(id) and i['age'] == age and i['gender'] != gender and i['city'] == city:
                            searching.append(i)
                    elif age == None and gender != None and city == None:
                        if int(i['id']) != int(id) and i['gender'] != gender:
                            searching.append(i)
                    elif age == None and gender != None and city != None:
                        if int(i['id']) != int(id) and i['gender'] != gender and i['city'] == city:
                            searching.append(i)
                    elif age != None and gender == None and city != None:
                        if int(i['id']) != int(id) and i['age'] == age and i['city'] == city:
                            searching.append(i)
                    elif age == None and gender == None and city != None:
                        if int(i['id']) != int(id) and i['city'] == city:
                            searching.append(i)
        if len(searching) > 0:
            two_id = random.choice(searching)
            users = vk.users.get(user_ids=f'{str(id)}, {str(two_id["id"])}')
            chat_one.append(two_id['id']); name_one.append(f'[id{str(id)}|{users[0]["first_name"]} {users[0]["last_name"]}]:')
            chat_two.append(id); name_two.append(f'[id{str(two_id["id"])}|{users[1]["first_name"]} {users[1]["last_name"]}]:')
            queue_chat.remove(two_id['id']); settings_chat.remove(one[0])
            queue_chat.remove(id); settings_chat.remove(two_id)
            set_razdel(id, 'open_chat')
            set_razdel(two_id['id'], 'open_chat')
            send_message(two_id['id'], 'Собеседник найден, приятного общения!\n\nЧтобы завершить диалог, нажми на кнопку снизу.',
                         keyboard=get_kb('open_chat'))
            send_message(id, 'Собеседник найден, приятного общения!\n\nЧтобы завершить диалог, нажми на кнопку снизу.',
                         keyboard=get_kb('open_chat'))

def stop_open(one_id, two_id):
    if one_id in queue_chat:
        settings_chat.remove(settings_chat[queue_chat.index(one_id)]); queue_chat.remove(one_id)
        set_razdel(one_id, 'general')
        send_message(one_id, 'Поиск завершен\n\n'+get_help('general'), get_kb('general'))
        if one_id in queue_likes:
            set_razdel(one_id, 'check_like')
            send_message(one_id, f'Тебя лайкнули {str(count_likes[queue_likes.index(one_id)])} пользователей!\n\n1. Показать', get_kb('check_like'))
            count_likes.remove(count_likes[queue_likes.index(one_id)])
            queue_likes.remove(one_id)
    else:
        if one_id in chat_one:
            name_one.remove(name_one[chat_one.index(one_id)]); name_two.remove(name_two[chat_two.index(two_id)])
            chat_one.remove(one_id); chat_two.remove(two_id)
        elif one_id in chat_two:
            name_one.remove(name_one[chat_one.index(two_id)]); name_two.remove(name_two[chat_two.index(one_id)])
            chat_one.remove(two_id); chat_two.remove(one_id)
        if one_id in queue_likes:
            set_razdel(one_id, 'check_like')
            send_message(one_id, f'Тебя лайкнули {str(count_likes[queue_likes.index(one_id)])} пользователей!\n\n1. Показать', get_kb('check_like'))
            count_likes.remove(count_likes[queue_likes.index(one_id)])
            queue_likes.remove(one_id)
        else:
            set_razdel(one_id, 'general')
            send_message(one_id, 'Диалог завершен.\n\n'+get_help('general'), keyboard=get_kb('general'))
        if two_id in queue_likes:
            set_razdel(two_id, 'check_like')
            send_message(two_id, f'Тебя лайкнули {str(count_likes[queue_likes.index(two_id)])} пользователей!\n\n1. Показать', get_kb('check_like'))
            count_likes.remove(count_likes[queue_likes.index(two_id)])
            queue_likes.remove(two_id)
        else:
            set_razdel(two_id, 'general')
            send_message(two_id, 'Собеседник завершил диалог.\n\n'+get_help('general'), keyboard=get_kb('general'))

def open_chat(id, msg):

    if id in chat_one:
        if len(msg)>0:
            two = chat_two[chat_one.index(id)]
            if msg.lower() == 'завершить':
                stop_open(id, two)
            else:
                send_message(two, f'{name_two[chat_two.index(two)]} {msg}', keyboard=get_kb('open_chat'))
    elif id in chat_two:
        if len(msg)>0:
            two = chat_one[chat_two.index(id)]
            if msg.lower() == 'завершить':
                stop_open(id, two)
            else:
                send_message(two, f'{name_one[chat_one.index(two)]} {msg}', keyboard=get_kb('open_chat'))
    else:
        send_message(id, 'Произошла ошибка.')
        set_razdel(id, 'general')
        send_message(id, get_help('general'), keyboard=get_kb('general'))



def send_message(peer_id, message, keyboard=None, attachment=None):
    vk.messages.send(
        peer_id=peer_id,
        random_id=0,
        message=message,
        keyboard=keyboard,
        attachment=attachment
    )

def upload_photo(upload, photo):
    response = upload.photo_messages(photo)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key



def new_handle(event):
    message = event.obj.message['text']
    peer_id = event.obj.message['peer_id']
    razd = get_razdel(peer_id)
    if len(message)>0:
        if message.split()[0].lower() == '/sendall':
            admins = get_admins(peer_id)
            if peer_id in admins:
                if len(message.split())>1:
                    send_message(peer_id, sending_all(peer_id, message[8:]))
                else:
                    send_message(peer_id, 'Команда: /sendall текст')
            else:
                pass
        elif message.split()[0].lower() == '/set_admin':
            if peer_id == get_owner():
                if len(message.split()) > 1:
                    id = 0
                    msg = message.split()[1]
                    if msg[0] == '[':
                        try:
                            id = int(msg[3:msg.index('|')])
                            send_message(peer_id, set_admin(peer_id, id))
                        except:
                            send_message(peer_id,
                                         'ID введен неправильно.\n\n/set_admin 1\n/set_admin @durov\n/set_admin vk.com/durov\n/set_admin http://vk.com/durov\n/set_admin https://vk.com/durov')
                    elif msg[0] == 'v':
                        try:
                            id = vk.users.get(user_ids=msg[7:])[0]['id']
                            send_message(peer_id, set_admin(peer_id, id))
                        except:
                            send_message(peer_id,
                                         'ID введен неправильно.\n\n/set_admin 1\n/set_admin @durov\n/set_admin vk.com/durov\n/set_admin http://vk.com/durov\n/set_admin https://vk.com/durov')
                    elif msg[0] == 'h':
                        try:
                            if msg[4] == 's':
                                id = vk.users.get(user_ids=msg[15:])[0]['id']
                                send_message(peer_id, set_admin(peer_id, id))
                            else:
                                id = vk.users.get(user_ids=msg[14:])[0]['id']
                                send_message(peer_id, set_admin(peer_id, id))
                        except:
                            send_message(peer_id,
                                         'ID введен неправильно.\n\n/set_admin 1\n/set_admin @durov\n/set_admin vk.com/durov\n/set_admin http://vk.com/durov\n/set_admin https://vk.com/durov')
                    else:
                        try:
                            int(msg)
                            send_message(peer_id, set_admin(peer_id, id))
                        except:
                            send_message(peer_id,
                                         'ID введен неправильно.\n\n/set_admin 1\n/set_admin @durov\n/set_admin vk.com/durov\n/set_admin http://vk.com/durov\n/set_admin https://vk.com/durov')
                else:
                    send_message(peer_id,
                                 'ID введен неправильно.\n\n/set_admin 1\n/set_admin @durov\n/set_admin vk.com/durov\n/set_admin http://vk.com/durov\n/set_admin https://vk.com/durov')
            else:
                pass
        elif message.split()[0].lower() == '/del_admin':
            if peer_id == get_owner():
                if len(message.split())>1:
                    id = 0
                    msg = message.split()[1]
                    if msg[0] == '[':
                        try:
                            id = int(msg[3:msg.index('|')])
                            send_message(peer_id, del_admin(peer_id, id))
                        except:
                            send_message(peer_id, 'ID введен неправильно.\n\n/del_admin 1\n/del_admin @durov\n/del_admin vk.com/durov\n/del_admin http://vk.com/durov\n/del_admin https://vk.com/durov')
                    elif msg[0] == 'v':
                        try:
                            id = vk.users.get(user_ids=msg[7:])[0]['id']
                            send_message(peer_id, del_admin(peer_id, id))
                        except:
                            send_message(peer_id, 'ID введен неправильно.\n\n/del_admin 1\n/del_admin @durov\n/del_admin vk.com/durov\n/del_admin http://vk.com/durov\n/del_admin https://vk.com/durov')
                    elif msg[0] == 'h':
                        try:
                            if msg[4] == 's':
                                id = vk.users.get(user_ids=msg[15:])[0]['id']
                                send_message(peer_id, del_admin(peer_id, id))
                            else:
                                id = vk.users.get(user_ids=msg[14:])[0]['id']
                                send_message(peer_id, del_admin(peer_id, id))
                        except:
                            send_message(peer_id, 'ID введен неправильно.\n\n/del_admin 1\n/del_admin @durov\n/del_admin vk.com/durov\n/del_admin http://vk.com/durov\n/del_admin https://vk.com/durov')
                    else:
                        try:
                            int(msg)
                            send_message(peer_id, del_admin(peer_id, id))
                        except:
                            send_message(peer_id, 'ID введен неправильно.\n\n/del_admin 1\n/del_admin @durov\n/del_admin vk.com/durov\n/del_admin http://vk.com/durov\n/del_admin https://vk.com/durov')
                else:
                    send_message(peer_id,
                                 'ID введен неправильно.\n\n/del_admin 1\n/del_admin @durov\n/del_admin vk.com/durov\n/del_admin http://vk.com/durov\n/del_admin https://vk.com/durov')
            else:
                pass
        elif message.lower() == '/get_admins':
            admins = get_admins(peer_id)
            msg = 'Админы бота:\n\n'
            if peer_id in admins:
                for i in admins:
                    msg+=f'vk.com/id{str(i)}\n'
                send_message(peer_id, msg)
            else:
                pass
        elif message.split()[0].lower() == '/set_owner':
            if peer_id == get_owner():
                if len(message.split()) > 1:
                    id = 0
                    msg = message.split()[1]
                    if msg[0] == '[':
                        try:
                            id = int(msg[3:msg.index('|')])
                            send_message(peer_id, get_owner(id))
                        except:
                            send_message(peer_id,
                                         'ID введен неправильно.\n\n/set_owner 1\n/set_owner @durov\n/set_owner vk.com/durov\n/set_owner http://vk.com/durov\n/set_owner https://vk.com/durov')
                    elif msg[0] == 'v':
                        try:
                            id = vk.users.get(user_ids=msg[7:])[0]['id']
                            send_message(peer_id, get_owner(id))
                        except:
                            send_message(peer_id,
                                         'ID введен неправильно.\n\n/set_owner 1\n/set_owner @durov\n/set_owner vk.com/durov\n/set_owner http://vk.com/durov\n/set_owner https://vk.com/durov')
                    elif msg[0] == 'h':
                        try:
                            if msg[4] == 's':
                                id = vk.users.get(user_ids=msg[15:])[0]['id']
                                send_message(peer_id, get_owner(id))
                            else:
                                id = vk.users.get(user_ids=msg[14:])[0]['id']
                                send_message(peer_id, get_owner(id))
                        except:
                            send_message(peer_id,
                                         'ID введен неправильно.\n\n/set_owner 1\n/set_owner @durov\n/set_owner vk.com/durov\n/set_owner http://vk.com/durov\n/set_owner https://vk.com/durov')
                    else:
                        try:
                            int(msg)
                            send_message(peer_id, get_owner(id))
                        except:
                            send_message(peer_id,
                                         'ID введен неправильно.\n\n/set_owner 1\n/set_owner @durov\n/set_owner vk.com/durov\n/set_owner http://vk.com/durov\n/set_owner https://vk.com/durov')
                else:
                    send_message(peer_id,
                                 'ID введен неправильно.\n\n/set_owner 1\n/set_owner @durov\n/set_owner vk.com/durov\n/set_owner http://vk.com/durov\n/set_owner https://vk.com/durov')
            else:
                pass

    if razd == 'general':
        if len(message)>0:
            if message[0] == '1' or message.lower() == 'перейти к анкетам':
                if check_profile(peer_id):
                    set_razdel(peer_id, 'set_search_1')
                    id_who_search.append(peer_id); param_search.append({'gender': '', 'age': '', 'city': '', 'done': False})
                    send_message(peer_id, 'Какой пол будем искать?\n\n1. Мужской\n2. Женский\n3. Неважно\n\n4. Отменить', keyboard=get_kb('set_search_1'))
                else:
                    set_razdel(peer_id, 'create_main')
                    send_message(peer_id, 'Чтобы смотреть анкеты, тебе нужно иметь анкету.\n\n1. Создать анкету\n2. Вернуться', keyboard=get_kb('create_main'))
            elif message[0] == '2' or message.lower() == 'найти чат':
                set_razdel(peer_id, 'set_open_1')
                send_message(peer_id,
                             'Хорошо! Укажи пол, по которому будем искать чат.\n\n1. Мужской\n2. Женский\n3. Неважно\n\n4. Отменить',
                             keyboard=get_kb('set_open_1'))
            elif message[0] == '3' or message.lower() == 'найти анонимный чат':
                set_razdel(peer_id, 'set_anon_1')
                send_message(peer_id, 'Хорошо! Укажи пол, по которому будем искать чат.\n\n1. Мужской\n2. Женский\n3. Неважно\n\n4. Отменить', keyboard=get_kb('set_anon_1'))
            elif message[0] == '4' or message.lower() == 'моя анкета':
                if check_profile(peer_id):
                    set_razdel(peer_id, 'my_anketa')
                    msg, photo = get_profile(peer_id)
                    send_message(peer_id, msg, attachment=photo)
                    send_message(peer_id, get_help('my_anketa'), keyboard=get_kb('my_anketa'))
                else:
                    set_razdel(peer_id, 'create_main')
                    send_message(peer_id, 'У тебя нет анкеты, давай создадим?\n\n1. Создать анкету\n2. Вернуться', get_kb('create_main'))
            elif message.lower() == 'начать':
                send_message(peer_id, f'Привет! Тебе доступны следующие команды:\n\n{get_help("general")}', get_kb('general'))
            else:
                send_message(peer_id, get_help("general"), get_kb('general'))
        else:
            send_message(peer_id, get_help('general'), get_kb('general'))
    elif razd == 'my_anketa':
        if len(message)>0:
            if message[0] == '1' or message.lower() == 'перейти к анкетам':
                if check_profile(peer_id):
                    set_razdel(peer_id, 'set_search_1')
                    id_who_search.append(peer_id)
                    param_search.append({'gender': '', 'age': '', 'city': '', 'done': False})
                    send_message(peer_id, 'Какой пол будем искать?\n\n1. Мужской\n2. Женский\n3. Неважно\n\n4. Отменить', keyboard=get_kb('set_search_1'))
                else:
                    set_razdel(peer_id, 'create_main')
                    send_message(peer_id, 'Чтобы смотреть анкеты, тебе нужно иметь анкету.\n\n1. Создать анкету', keyboard=get_kb('create_main'))
            elif message[0] == '2' or message.lower() == 'изменить имя':
                if check_profile(peer_id):
                    set_razdel(peer_id, 'change_name')
                    id_change.append(peer_id)
                    date_change.append('name')
                    send_message(peer_id, 'Хорошо, теперь укажи новое имя.\n\n1. Отменить', keyboard=get_kb('change_name'))
                else:
                    pass
            elif message[0] == '3' or message.lower() == 'изменить возраст':
                if check_profile(peer_id):
                    set_razdel(peer_id, 'change_age')
                    id_change.append(peer_id)
                    date_change.append('age')
                    send_message(peer_id, 'Хорошо, теперь укажи новый возраст.\n\n1. Отменить', keyboard=get_kb('change_age'))
                else:
                    pass
            elif message[0] == '4' or message.lower() == 'изменить город':
                if check_profile(peer_id):
                    set_razdel(peer_id, 'change_city')
                    id_change.append(peer_id)
                    date_change.append('city')
                    send_message(peer_id, 'Хорошо, теперь укажи новый город.\n\n1. Отменить', keyboard=get_kb('change_city'))
                else:
                    pass
            elif message[0] == '5' or message.lower() == 'изменить текст':
                if check_profile(peer_id):
                    set_razdel(peer_id, 'change_text')
                    id_change.append(peer_id)
                    date_change.append('text')
                    send_message(peer_id, 'Хорошо, теперь укажи новый текст.\n\n1. Не указывать текст\n2. Отменить', keyboard=get_kb('change_text'))
                else:
                    pass
            elif message[0] == '6' or message.lower() == 'изменить картинку':
                if check_profile(peer_id):
                    set_razdel(peer_id, 'change_photo')
                    id_change.append(peer_id)
                    date_change.append('photo')
                    send_message(peer_id, 'Хорошо, теперь пришли новую картинку.\n\n1. Отменить', keyboard=get_kb('change_photo'))
                else:
                    pass
            elif message[0] == '7' or message.lower() == 'удалить анкету':
                if check_profile(peer_id):
                    set_razdel(peer_id, 'create_main')
                    del_profile(peer_id)
                    send_message(peer_id, 'Анкета удалена!\n')
                else:
                    pass
            elif message[0] == '8' or message.lower() == 'главное меню':
                set_razdel(peer_id, 'general')
                send_message(peer_id, get_help('general'), get_kb('general'))
            else:
                send_message(peer_id, get_help('my_anketa'), keyboard=get_kb('my_anketa'))
        else:
            send_message(peer_id, get_help('my_anketa'), keyboard=get_kb('my_anketa'))
    elif razd == 'create_main':
        if len(message)>0:
            if message[0] == '1' or message.lower() == 'создать анкету' or message.lower() == 'создать' or message.lower() == 'создать новую':
                set_razdel(peer_id, 'create_1')
                send_message(peer_id,
                             'Отлично!\n\nДля начала укажи свой пол.\n\n1. Мужской\n2. Женский',
                             keyboard=get_kb('create_1'))
                queue.append(peer_id); stage.append('gender')
                date.append({'id': peer_id, 'age': 0, 'gender': '', 'city': '', 'name': '', 'text': '', 'photo': ''})
            elif message[0] == '2' or message.lower() == 'вернуться':
                set_razdel(peer_id, 'general')
                send_message(peer_id, get_help('general'), get_kb('general'))
            else:
                send_message(peer_id,
                             'Чтобы смотреть анкеты, тебе нужно иметь анкету.\n\n1. Создать анкету\n2. Вернуться',
                             keyboard=get_kb('create_main'))
        else:
            send_message(peer_id, 'Чтобы смотреть анкеты, тебе нужно иметь анкету.\n\n1. Создать анкету\n2. Вернуться',
                         keyboard=get_kb('create_main'))
    elif razd == 'create_1':
        if len(message)>0:
            if message[0] == '1':
                send_message(peer_id, create_profile(peer_id, 'мужской'))
            elif message[0] == '2':
                send_message(peer_id, create_profile(peer_id, 'женский'))
            elif message.lower() == 'мужской' or message.lower() == 'женский':
                send_message(peer_id, create_profile(peer_id, message))
        else:
            send_message(peer_id,
                         'Для начала укажи свой пол.\n\n1. Мужской\n2. Женский',
                         keyboard=get_kb('create_1'))
    elif razd == 'create_4':
        send_message(peer_id, create_profile(peer_id, message), keyboard=get_kb('create_5'))
    elif razd == 'create_2' or razd == 'create_3' or razd == 'create_5':
        send_message(peer_id, create_profile(peer_id, message))
    elif razd == 'create_6':
        send_message(peer_id, create_profile(peer_id, event))
    elif razd == 'set_anon_1':
        if len(message)>0:
            if message[0] == '1' or message.lower() == 'мужской':
                send_message(peer_id, set_anon(peer_id, 'мужской'), keyboard=get_kb(get_razdel(peer_id)))
            elif message[0] == '2' or message.lower() == 'женский':
                send_message(peer_id, set_anon(peer_id, 'женский'), keyboard=get_kb(get_razdel(peer_id)))
            elif message[0] == '3' or message.lower() == 'неважно':
                send_message(peer_id, set_anon(peer_id, 'неважно'), keyboard=get_kb(get_razdel(peer_id)))
            elif message[0] == '4' or message.lower() == 'отменить':
                set_anon(peer_id, 'отменить')
            elif message.lower() == 'мужской' or message.lower() == 'женский' or message.lower() == 'неважно' or message.lower() == 'отменить':
                send_message(peer_id, set_anon(peer_id, message), keyboard=get_kb(get_razdel(peer_id)))
            else:
                send_message(peer_id,
                             'Выбери нужный вариант ответа.\n\n1. Мужской\n2. Женский\n3. Неважно\n\n4. Отменить',
                             keyboard=get_kb(get_razdel(peer_id)))
        else:
            send_message(peer_id, 'Выбери нужный вариант ответа.\n\n1. Мужской\n2. Женский\n3. Неважно\n\n4. Отменить',
                         keyboard=get_kb(get_razdel(peer_id)))
    elif razd == 'set_anon_2':
        if len(message)>0:
            if message == '1' or message == '0-17':
                send_message(peer_id, set_anon(peer_id, '0-17'), keyboard=get_kb(get_razdel(peer_id)))
            elif message == '2' or message == '18-29':
                send_message(peer_id, set_anon(peer_id, '18-29'), keyboard=get_kb(get_razdel(peer_id)))
            elif message == '3' or message == '30+':
                send_message(peer_id, set_anon(peer_id, '30+'), keyboard=get_kb(get_razdel(peer_id)))
            elif message == '4' or message.lower() == 'неважно':
                send_message(peer_id, set_anon(peer_id, 'неважно'), keyboard=get_kb(get_razdel(peer_id)))
            elif message == '5' or message.lower() == 'отменить':
                set_anon(peer_id, 'отменить')
            else:
                send_message(peer_id, set_anon(peer_id, message), keyboard=get_kb(get_razdel(peer_id)))
        else:
            send_message(peer_id, 'Выбери нужный вариант ответа.\n\n1. 0-17\n2. 18-29\n3. 30+\n4. Неважно\n\n5. Отменить', keyboard=get_kb(get_razdel(peer_id)))
    elif razd == 'set_anon_3':
        if len(message)>0:
            if message[0] == '1' or message.lower() == 'неважно':
                send_message(peer_id, set_anon(peer_id, 'неважно'), keyboard=get_kb(get_razdel(peer_id)))
            elif message[0] == '2' or message.lower() == 'отменить':
                set_anon(peer_id, 'отменить')
            else:
                send_message(peer_id, set_anon(peer_id, message), keyboard=get_kb(get_razdel(peer_id)))
            if get_razdel(peer_id) == 'wait_anon':
                start_anon(peer_id)
        else:
            send_message(peer_id, 'Выбери нужный вариант ответа.\n\n1. Неважно\n2. Отменить', keyboard=get_kb(get_razdel(peer_id)))
    elif razd == 'wait_anon':
        if len(message)>0:
            if message[0] == '1' or message.lower() == 'отменить':
                stop_anon(peer_id, peer_id)
        else:
            send_message(peer_id, 'Поиск собеседника 🧸\n\n1. Отменить', get_kb('wait_anon'))
    elif razd == 'anon_chat':
        if len(message)>0:
            anon_chat(peer_id, message)
    elif razd == 'open_chat':
        if len(message)>0:
            open_chat(peer_id, message)
    elif razd == 'set_open_1':
            if len(message) > 0:
                if message[0] == '1' or message.lower() == 'мужской':
                    send_message(peer_id, set_open(peer_id, 'мужской'), keyboard=get_kb(get_razdel(peer_id)))
                elif message[0] == '2' or message.lower() == 'женский':
                    send_message(peer_id, set_open(peer_id, 'женский'), keyboard=get_kb(get_razdel(peer_id)))
                elif message[0] == '3' or message.lower() == 'неважно':
                    send_message(peer_id, set_open(peer_id, 'неважно'), keyboard=get_kb(get_razdel(peer_id)))
                elif message[0] == '4' or message.lower() == 'отменить':
                    set_open(peer_id, 'отменить')
                elif message.lower() == 'мужской' or message.lower() == 'женский' or message.lower() == 'неважно' or message.lower() == 'отменить':
                    send_message(peer_id, set_open(peer_id, message), keyboard=get_kb(get_razdel(peer_id)))
                else:
                    send_message(peer_id, 'Выбери нужный вариант ответа.\n\n1. Мужской\n2. Женский\n3. Неважно\n\n4. Отменить',
                                 keyboard=get_kb(get_razdel(peer_id)))
            else:
                send_message(peer_id, 'Выбери нужный вариант ответа.\n\n1. Мужской\n2. Женский\n3. Неважно\n\n4. Отменить',
                             keyboard=get_kb(get_razdel(peer_id)))
    elif razd == 'set_open_2':
            if len(message) > 0:
                if message == '1' or message == '0-17':
                    send_message(peer_id, set_open(peer_id, '0-17'), keyboard=get_kb(get_razdel(peer_id)))
                elif message == '2' or message == '18-29':
                    send_message(peer_id, set_open(peer_id, '18-29'), keyboard=get_kb(get_razdel(peer_id)))
                elif message == '3' or message == '30+':
                    send_message(peer_id, set_open(peer_id, '30+'), keyboard=get_kb(get_razdel(peer_id)))
                elif message == '4' or message.lower() == 'неважно':
                    send_message(peer_id, set_open(peer_id, 'неважно'), keyboard=get_kb(get_razdel(peer_id)))
                elif message == '5' or message.lower() == 'отменить':
                    set_open(peer_id, 'отменить')
                else:
                    send_message(peer_id, set_open(peer_id, message), keyboard=get_kb(get_razdel(peer_id)))
            else:
                send_message(peer_id,
                             'Выбери нужный вариант ответа.\n\n1. 0-17\n2. 18-29\n3. 30+\n4. Неважно\n\n5. Отменить',
                             keyboard=get_kb(razd))
    elif razd == 'set_open_3':
            if len(message) > 0:
                if message[0] == '1' or message.lower() == 'неважно':
                    send_message(peer_id, set_open(peer_id, 'неважно'), keyboard=get_kb(get_razdel(peer_id)))
                elif message[0] == '2' or message.lower() == 'отменить':
                    set_open(peer_id, 'отменить')
                else:
                    send_message(peer_id, set_open(peer_id, message), keyboard=get_kb(get_razdel(peer_id)))
                if get_razdel(peer_id) == 'wait_open':
                    start_open(peer_id)
            else:
                send_message(peer_id, 'Выбери нужный вариант ответа.\n\n1. Неважно\n2. Отменить', keyboard=get_kb(get_razdel(peer_id)))
    elif razd == 'wait_open':
        if len(message)>0:
            if message[0] == '1' or message.lower() == 'отменить':
                stop_open(peer_id, peer_id)
        else:
            send_message(peer_id, 'Поиск собеседника 🧸\n\n1. Отменить', get_kb('wait_open'))
    elif razd == 'set_search_1':
        if len(message)>0:
            if message == '1' or message.lower() == 'мужской':
                set_search(peer_id, 'Мужской')
            elif message == '2' or message.lower() == 'женский':
                set_search(peer_id, 'Женский')
            elif message == '3' or message.lower() == 'неважно':
                set_search(peer_id, 'Неважно')
            elif message == '4' or message.lower() == 'отменить':
                set_search(peer_id, 'Отменить')
            else:
                set_search(peer_id, message)
        else:
            send_message(peer_id, 'Выбери нужный вариант ответа.\n\n1. Мужской\n2. Женский\n3. Неважно\n\n4. Отменить', keyboard=get_kb('set_search_1'))
    elif razd == 'set_search_2':
        if len(message)>0:
            if message == '1' or message == '0-17':
                set_search(peer_id, '0-17')
            elif message == '2' or message == '18-29':
                set_search(peer_id, '18-29')
            elif message == '3' or message == '30+':
                set_search(peer_id, '30+')
            elif message == '4' or message.lower() == 'неважно':
                set_search(peer_id, 'Неважно')
            elif message == '5' or message.lower() == 'отменить':
                set_search(peer_id, 'Отменить')
            else:
                set_search(peer_id, message)
        else:
            send_message(peer_id, 'Выбери нужный вариант ответа.\n\n1. 0-17\n2. 18-29\n3. 30+\n4. Неважно\n\n5. Отменить', keyboard=get_kb('set_search_2'))
    elif razd == 'set_search_3':
        if len(message)>0:
            if message == '1' or message.lower() == 'неважно':
                set_search(peer_id, 'Неважно')
            elif message == '2' or message.lower() == 'отменить':
                set_search(peer_id, 'Отменить')
            else:
                set_search(peer_id, message)
        else:
            send_message(peer_id, 'Выбери правильный вариант ответа или напиши нужный город.\n\n1. Неважно\n2. Отменить', keyboard=get_kb('set_search_3'))
    elif razd == 'searching':
        if message.lower() == 'завершить':
            pass
        elif message == '👍':
            like(peer_id)
            ind = id_who_search.index(peer_id)
            search(peer_id, param_search[ind]['age'], param_search[ind]['gender'], param_search[ind]['city'])
        elif message == '👎':
            ind = id_who_search.index(peer_id)
            search(peer_id, param_search[ind]['age'], param_search[ind]['gender'], param_search[ind]['city'])
        elif message == '💌':
            like(peer_id, send=True)
        elif message == '💤':
            ind = id_who_search.index(peer_id)
            param_search.remove(param_search[ind]); id_who_search.remove(peer_id)
            id_searched.remove(id_searched[id_searching.index(peer_id)]); id_searching.remove(peer_id)
            if peer_id in queue_likes:
                set_razdel(peer_id, 'check_like')
                send_message(peer_id, f'Тебя лайкнули {str(count_likes[queue_likes.index(peer_id)])} пользователей!\n\n1. Показать', get_kb('check_like'))
                count_likes.remove(count_likes[queue_likes.index(peer_id)])
                queue_likes.remove(peer_id)
            else:
                set_razdel(peer_id, 'general')
                send_message(peer_id, get_help('general'), get_kb('general'))
    elif razd == 'send_like':
        if len(message)>0:
            if message.lower() == 'отменить' or message == '1':
                set_razdel(peer_id, 'searching')
                send_message(peer_id, get_profile(id_searched[id_searching.index(peer_id)]), keyboard=get_kb('searching'))
            else:
                like(peer_id, message=message)
                set_razdel(peer_id, 'searching')
                ind = id_who_search.index(peer_id)
                search(peer_id, param_search[ind]['age'], param_search[ind]['gender'], param_search[ind]['city'])
        else:
            send_message(peer_id, 'Пришли сообщение текстом.', get_kb('send_like'))
    elif razd == 'show_like':
        if message == '👍':
            show_like(peer_id, 'like')
        elif message == '👎':
            show_like(peer_id, 'dis')
        else:
            show_like(peer_id, 'show')
    elif razd == 'check_like':
        if len(message)>0:
            if message[0] == '1' or message.lower() == 'показать':
                set_razdel(peer_id, 'show_like')
                show_like(peer_id, 'show')
            else:
                send_message(peer_id, 'Выбери нужный вариант ответа.\n\n1. Показать', keyboard=get_kb('check_like'))
        else:
            send_message(peer_id, 'Выбери нужный вариант ответа.\n\n1. Показать', keyboard=get_kb('check_like'))
    elif razd == 'change_age' or razd == 'change_name' or razd == 'change_city' or 'change_text' or 'change_photo':
        result = False
        if len(message)>0:
            if razd != 'change_text':
                if message.lower() == 'отменить' or message == '1':
                    date_change.remove(date_change[id_change.index(peer_id)]); id_change.remove(peer_id)
                    msg, photo = get_profile(peer_id)
                    set_razdel(peer_id, 'my_anketa')
                    send_message(peer_id, msg, attachment=photo)
                    send_message(peer_id, get_help('my_anketa'), get_kb('my_anketa'))
            elif razd == 'change_text':
                if message.lower() == 'не указывать текст' or message == '1':
                    result = change_profile(peer_id, date_change[id_change.index(peer_id)], '',
                                            event.obj.message['attachments'])
                elif message.lower() == 'отменить' or message == '2':
                    date_change.remove(date_change[id_change.index(peer_id)])
                    id_change.remove(peer_id)
                    msg, photo = get_profile(peer_id)
                    set_razdel(peer_id, 'my_anketa')
                    send_message(peer_id, msg, attachment=photo)
                    send_message(peer_id, get_help('my_anketa'), get_kb('my_anketa'))
                else:
                    result = change_profile(peer_id, date_change[id_change.index(peer_id)], message,
                                            event.obj.message['attachments'])
            else:
                result = change_profile(peer_id, date_change[id_change.index(peer_id)], message,
                                        event.obj.message['attachments'])
        if result != False:
            if result == True:
                date_change.remove(date_change[id_change.index(peer_id)]); id_change.remove(peer_id)
                msg, photo = get_profile(peer_id)
                send_message(peer_id, 'Анкета изменена 👇')
                send_message(peer_id, msg, attachment=photo)
                send_message(peer_id, get_help('my_anketa'), get_kb('my_anketa'))
                set_razdel(peer_id, 'my_anketa')
            else:
                send_message(peer_id, result, keyboard=get_kb(get_razdel(peer_id)))


def main():
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                # print(event)
                try:
                    if event.obj.message['from_id'] == event.obj.message['peer_id']:
                        print(event)
                        new_handle(event)
                except Exception as err:
                    print(err)
    except:
        main()

main()
