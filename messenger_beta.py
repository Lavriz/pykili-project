import re
import os.path
import datetime
import csv

def logpass_receive():
    with open('logpass.csv','r',encoding='utf-8') as auth_file:
        reader = csv.reader(auth_file)
        auth_dict = {}
        for row in reader:
            try:
                auth_dict[row[0]]=row[1]
            except IndexError:
                break
    return auth_dict

def first_check(auth_dict):
    if auth_dict == {}:
        print('There are no accounts yet. Be our first user!')
        login_line = ''
    else: 
        login_line = input('Enter your username. If you don\'t have an account, press Enter:\n')
    return login_line

def create_new_acc(auth_dict):
    print('Enter your new username (Should be 6 to 30 characters; may contain numbers, latin letters, hyphen(-) and underscore(_) characters):')
    while True:
        while True:
            new_login = input()
            if not re.fullmatch('[0-9A-Za-z_\-]{6,30}',new_login):
                print('Please choose a valid username:')
                continue
            break
        name_is_free = True
        for key in auth_dict:
            if new_login == key:
                print('This username is taken; try another one:\n')
                name_is_free = False
        if  name_is_free:
            print('Enter your new password. It may contain numbers and capital and small letters and should be at least 8 characters long:')
            while True:
                new_pass = input()
                if new_pass == '' or not re.fullmatch('[0-9A-Za-z]{8,}',new_pass):
                    print('Please choose a valid password')
                    continue
                break
            auth_dict[new_login] = new_pass
            with open('logpass.csv','w',encoding='utf-8') as auth_file:
                writer = csv.writer(auth_file,quoting=csv.QUOTE_ALL)
                for key in auth_dict:
                    line = (key,auth_dict[key])
                    writer.writerow(line)
            print('Congrats on your new account, ',new_login,'!',sep='')
            user = new_login
            break
    return user

def check_existing_log(login_line,auth_dict):
    while True:
        correct_login = False
        for key in auth_dict:
            if key == login_line:
                correct_login = True
        if not correct_login:
            print('Username incorrect or doesn\'t exist. Try again:')
            login_line = input()
            continue
        if correct_login:
            break
    print('Enter your password:')
    while True:
        pass_line = input()
        if pass_line == auth_dict[login_line]:
            print('Authentication complete; Greetings, ',login_line,'!',sep='')
            user = login_line
            break
        else:
            print('Incorrect password,try again:')
    return user

def authenticate_user():
    auth_dict = logpass_receive()
    login_line = first_check(auth_dict)
    if login_line == '':
        online_user = create_new_acc(auth_dict)
    else:
        online_user = check_existing_log(login_line,auth_dict)
    return online_user, auth_dict

# ACCOUNT INTERFACE

def choose_option():
    while True:
        print('Select one of a few options by printing the corresponding number:\n')
        print('1. Open chats\n2. Account settings\n3. Log out\n')
        chosen = input()
        if not re.fullmatch('[1-3]',chosen):
            print('Choose a valid option please\n')
            continue
        return chosen

# MESSAGING

def tag_read(online_user,auth_dict):
    timed_list = []
    sorted_list = []
    with open('tags.csv','r',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                if re.search(online_user,row[0]):
                    timed_list.append(row)
            except IndexError:
                return None
        timed_list = sorted(timed_list,key=lambda timed_line: timed_line[3],reverse = True)
        for i in timed_list:
            for key in auth_dict:
                if key == online_user:
                    continue
                if re.search(key,i[0]):
                    if i[2] != online_user:
                            sorted_list.append([key,'0'])
                    else:
                        sorted_list.append([key,i[1]])
        return sorted_list

def chat_create(online_user,auth_dict):
    sorted_list = tag_read(online_user,auth_dict)
    print(sorted_list)
    while True:
        print('Select user to chat with:\n')
        if len(auth_dict) == 1:
            return online_user, None
        if sorted_list: 
            for i in sorted_list:
                if i[1] == '0':
                    print(i[0])
                else:
                    print(i[0],'–',i[1],'new')
        for key in auth_dict:
            already_shown = False
            if key == online_user:
                continue
            if sorted_list:
                for i in sorted_list:
                    if key == i[0]:
                        already_shown = True
            if not already_shown:
                print(key)
        while True:
            address = input('Type the user in: ')
            if address == online_user:
                print('You can\'t chat with yourself (yet)')
                continue
            break
        address_match = False
        for key in auth_dict:
            if address == key:
                address_match = True
                break
        if not address_match:
            print('Enter a real username\n')
        if address_match:
            return online_user, address

def tag_apply(user_pair,new_messages,direction,last_message):
    user_join = '='.join(user_pair)
    lines = []
    with open('tags.csv','r',encoding='utf-8') as file:
        reader = csv.reader(file)
        updated = False
        for row in reader:
            try:
                if user_join == row[0]:
                    if last_message == '':
                        last_message = row[3]
                    if direction == row[2]:
                        new_messages = new_messages + int(row[1])
                    lines.append([user_join,new_messages,direction,last_message])
                    updated = True
                else:
                    lines.append(row)
            except IndexError:
                break
        if not updated:
            lines.append([user_join,new_messages,direction,last_message])
    with open('tags.csv','w',encoding='utf-8') as file:
        writer = csv.writer(file,quoting=csv.QUOTE_ALL)
        for line in lines:
            writer.writerow(line)

def message_writing(online_user,address):
    user_pair = sorted((online_user,address))
    filename = ''.join(('chats/','='.join(user_pair),'.txt'))
    file_exists = os.path.exists(filename)
    if file_exists:
        with open(filename,'r',encoding='utf-8') as file:
            print(file.read())
    with open(filename,'a',encoding='utf-8') as file:
        new_messages = 0
        last_message = ''
        while True:
            entered = input('You: ')
            if re.fullmatch('\s*',entered):
                print('Enter a valid message')
                continue
            if entered == '/endsession':
                tag_apply(user_pair,new_messages,address,last_message)
                break
            new_messages += 1
            last_message = datetime.datetime.now()
            file.write(''.join((online_user,': ',entered,'\n')))


# MAIN PROGRAM

online,dic = authenticate_user()
while True:
    chosen = choose_option()
    if chosen == '1':
        user,receiver = chat_create(online,dic)
        if not receiver:
            print('There are no other users yet.')
            continue
        else:
            message_writing(user,receiver)
    if chosen == '2':
        print('Settings will be here soon')
    if chosen == '3':
        print('Goodbye,',online)
        break
