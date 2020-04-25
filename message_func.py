import re
import os.path
import datetime
import csv

def get_user(user):
    with open('logpass.csv','r',encoding='utf-8') as file:
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
    with open('logpass.csv','r',encoding='utf-8') as file:
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
    with open('logpass.csv','w',encoding='utf-8') as file:
        writer = csv.writer(file,quoting=csv.QUOTE_ALL)
        for entry in table:
            line = (entry['username'],entry['password'])
            print(line)
            writer.writerow(line)

def chat_list(online_user):
    with open('logpass.csv','r',encoding='utf-8') as file:
        reader = csv.reader(file)
        users = []
        for row in reader:
            try:
                if row[0] != online_user:
                    users.append(row[0])
            except IndexError:
                break
    return users

def chatTag_table_receive():
    tag_table = []
    with open('tags.csv','r',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            tag_dict = {}
            try:
                tag_dict['chat'] = row[0]
                tag_dict['new'] = row[1]
                tag_dict['direction'] = row[2]
                tag_dict['last'] = row[3]
                tag_table.append(tag_dict)
            except IndexError:
                return None
        tag_table = sorted(tag_table,key=lambda tag_entry: tag_entry['last'],reverse = True)
        return tag_table
