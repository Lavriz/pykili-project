import re
import os
import csv

def comply_login(login):
    if not re.fullmatch('[0-9A-Za-z][0-9A-Za-z_\-]{3,30}',login):
        return False
    return True

def comply_pass(password):
    if not re.fullmatch('[0-9A-Za-z]{8,}',password):
        return False
    return True


def get_user(user):
    with open('data/logpass.csv','r',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                if row[0] == user:
                    return row[1]
            except IndexError:
                break
        return None

def add_user(user,password):
    table = []
    with open('data/logpass.csv','r',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            entry = {}
            try:
                entry['username'] = row[0]
                entry['password'] = row[1]
                table.append(entry)
            except IndexError:
                break
    new_entry = {}
    new_entry['username'] = user
    new_entry['password'] = password
    table.append(new_entry)
    with open('data/logpass.csv','w',encoding='utf-8') as file:
        writer = csv.writer(file,quoting=csv.QUOTE_ALL)
        for entry in table:
            line = (entry['username'],entry['password'])
            writer.writerow(line)

def remove_user(user):
    table = []
    with open('data/logpass.csv','r',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            entry = {}
            try:
                entry['username'] = row[0]
                entry['password'] = row[1]
                table.append(entry)
            except IndexError:
                break
    i = 0
    for entry in table:
        if entry['username'] == user:
            removed = table.pop(i)
            break
        i += 1
    with open('data/logpass.csv','w',encoding='utf-8') as file:
        writer = csv.writer(file,quoting=csv.QUOTE_ALL)
        for entry in table:
            line = (entry['username'],entry['password'])
            print(line)
            writer.writerow(line)

def chat_list(online_user):
    with open('data/logpass.csv','r',encoding='utf-8') as file:
        reader = csv.reader(file)
        users = []
        for row in reader:
            try:
                if row[0] != online_user:
                    users.append(row[0])
            except IndexError:
                break
    return users

def create_pair(username,login):
    user_pair = '='.join(sorted([username,login]))
    return user_pair

def save_message(pair, json):
    author = json['user_name']
    message = json['message']
    filename = 'data/chat_history/' + pair + '.csv'
    entry = (author, message)
    with open(filename,'a',encoding='utf-8') as file:
        writer = csv.writer(file,quoting=csv.QUOTE_ALL)
        writer.writerow(entry)

def read_chat(pair):
    filename = 'data/chat_history/' + pair + '.csv'
    file_exists = os.path.exists(filename)
    history = {}
    if file_exists:
        with open(filename,'r',encoding='utf-8') as file:
            reader = csv.reader(file)
            i = 0
            try:
                for row in reversed(list(reader)):
                    di = {}
                    di['author'] = row[0]
                    di['message'] = row[1]
                    history[i] = di
                    i += 1
            except IndexError:
                return history
    return history

def add_groupchat(groupname, user_list, online_user):
    line = [groupname, online_user]
    for i in range(0,len(user_list)):
        line.append(user_list[i])
    with open('data/groupchats.csv','a',encoding='utf-8') as file:
        writer = csv.writer(file,quoting=csv.QUOTE_ALL)
        writer.writerow(line)

def read_groupchat(group):
    filename = 'data/groupchat_history/' + group + '.csv'
    file_exists = os.path.exists(filename)
    history = {}
    if file_exists:
        with open(filename,'r',encoding='utf-8') as file:
            reader = csv.reader(file)
            i = 0
            try:
                for row in reversed(list(reader)):
                    di = {}
                    di['author'] = row[0]
                    di['message'] = row[1]
                    history[i] = di
                    i += 1
            except IndexError:
                return history
    return history

def save_groupmessage(group, json):
    author = json['user_name']
    message = json['message']
    filename = 'data/groupchat_history/' + group + '.csv'
    entry = (author, message)
    with open(filename,'a',encoding='utf-8') as file:
        writer = csv.writer(file,quoting=csv.QUOTE_ALL)
        writer.writerow(entry)

def groupchat_list(user):
    with open('data/groupchats.csv','r',encoding='utf-8') as file:
        reader = csv.reader(file)
        group_list = []
        try:
            for row in reader:
                for i in range (1,len(row)):
                    try:
                        if row[i] == user:
                            group_list.append(row[0])
                        i += 1
                    except IndexError:
                        break
        except IndexError:
            return group_list
        return group_list

def groupchat_history(groupname):
    filename = 'data/groupchat_history/' + groupname + '.csv'
    file_exists = os.path.exists(filename)
    history = {}
    if file_exists:
        with open(filename,'r',encoding='utf-8') as file:
            reader = csv.reader(file)
            i = 0
            try:
                for row in reversed(list(reader)):
                    di = {}
                    di['author'] = row[0]
                    di['message'] = row[1]
                    history[i] = di
                    i += 1
            except IndexError:
                return history
    return history

def remove_chat(filename, groupname):
    current_dir = os.getcwd()
    to_delete = current_dir + filename
    try:
        os.remove(to_delete)
    except FileNotFoundError:
        print('no history')
    with open('data/groupchats.csv','r',encoding='utf-8') as file:
        reader = csv.reader(file)
        li = []
        for row in reader:
            print(list(row))
            li.append(list(row))
        for i in range(0,len(li)):
            try:
                print(li[i])
                if li[i][0] == groupname:
                    li.pop(i)
            except IndexError:
                break
        print(li)
    with open('data/groupchats.csv','w',encoding='utf-8') as file:
        writer = csv.writer(file,quoting=csv.QUOTE_ALL)
        for entry in li:
            writer.writerow(entry)
