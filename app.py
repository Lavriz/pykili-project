from flask import Flask, render_template, request, redirect, url_for, session
from message_func import comply_login, comply_pass, get_user, add_user, remove_user, chat_list, create_pair, save_message, read_chat, groupchat_history, add_groupchat, groupchat_list, save_groupmessage, remove_chat
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/',methods=['GET','POST'])
def login():
    if 'login' in session:
        return redirect('/chats')
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        check = get_user(login)
        if not check:
            error = 'Username not found'
            return render_template('home.html',error=error)
        if password == check:
            session['login'] = login
            return redirect('/chats')
        elif password == '':
            error = 'Password field empty'
            return render_template('home.html',error=error)
        else:
            error = 'Incorrect password'
            return render_template('home.html',error=error)
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('login',None)
    return redirect('/')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        new_log = request.form['new_log']
        new_pass = request.form['new_pass']
        confirm = request.form['confirm']
        check = get_user(new_log)
        if check:
            error = 'Username exists'
            return render_template('signup.html',error=error)
        if not comply_login(new_log):
            error = 'Invalid login'
            return render_template('signup.html',error=error)
        if new_pass == '':
            error = 'Enter a password'
            return render_template('signup.html',error=error)
        if not comply_pass(new_pass):
            error = 'Invalid password'
            return render_template('signup.html',error=error)
        if new_pass != confirm:
            error = 'Passwords do not match'
            return render_template('signup.html',error=error)
        add_user(new_log,new_pass)
        session['login'] = new_log
        return redirect('/chats')
    return render_template('signup.html')

@app.route('/chats')
def chats():
    if not 'login' in session:
        return redirect('/')
    auth_base = chat_list(session['login'])
    group_base = groupchat_list(session['login'])
    try:
        session.pop('receiver',None)
    except KeyError:
        print('no receiver')
    return render_template('chats.html', auth_base = auth_base, group_base = group_base, login=session['login'])

@app.route('/delete')
def settings():
    return render_template('deleting.html', login = session['login'])

@app.route('/delete/confirm')
def deleting():
    remove_user(session['login'])
    return redirect('/logout')

@app.route('/chats/groupcreate', methods=['GET','POST'])
def create_groupchat():
    auth_base = chat_list(session['login'])
    if request.method == 'POST':
        groupname = request.form['groupname']
        invite_list = []
        for user in auth_base:
            try:
                invite_list.append(request.form[user])
            except KeyError:
                continue
        if groupname == '':
            error = 'Enter a name, please'
            return render_template('groupcreate.html', auth_base = auth_base, error = error)
        if invite_list == []:
            error = 'Select users, please'
            return render_template('groupcreate.html', auth_base = auth_base, error = error)
        add_groupchat(groupname,invite_list,session['login'])
        return redirect('/chats')
    return render_template('groupcreate.html', auth_base = auth_base)

@app.route('/chats/group/<string:groupname>', methods = ['GET','POST'])
def group_chat(groupname):
    history = groupchat_history(groupname)
    presented = []
    try:
        if len(history) > 50:
            for i in range(49,-1,-1):
                presented.append(history[i]['author'] + ': ' + history[i]['message'])
        elif len(history) <= 50:
            for i in range(len(history)-1,-1,-1):
                presented.append(history[i]['author'] + ': ' + history[i]['message'])
    except IndexError:
        presented = []
    session['receiver'] = groupname
    return render_template('group.html', login = session['login'], receiver = session['receiver'], hist_list = presented)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route('/chats/group/<string:groupname>/delete')
def delete_groupchat(groupname):
    filename = '/data/groupchat_history/' + groupname + '.csv'
    remove_chat(filename, groupname)
    return redirect('/chats')


@app.route('/chats/<string:username>', methods = ['GET','POST'])
def user_chat(username):
    history = read_chat(create_pair(username,session['login']))
    presented = []
    try:
        if len(history) > 50:
            for i in range(49,-1,-1):
                presented.append(history[i]['author'] + ': ' + history[i]['message'])
        elif len(history) <= 50:
            for i in range(len(history)-1,-1,-1):
                presented.append(history[i]['author'] + ': ' + history[i]['message'])
    except IndexError:
        presented = []
    session['receiver'] = username
    return render_template('personal.html', login = session['login'], receiver = session['receiver'], hist_list = presented)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('personal')
def handle_personal_message(json, methods=['GET', 'POST']):
    print('received message: ' + str(json))
    room = create_pair(session['receiver'],session['login'])
    try:
        save_message(room, json)
    except KeyError:
        print('oops')
    join_room(room)
    socketio.emit('response', json, room = room, callback=messageReceived)

@socketio.on('group')
def handle_personal_message(json, methods=['GET', 'POST']):
    print('received message: ' + str(json))
    room = session['receiver']
    try:
        save_groupmessage(room, json)
    except KeyError:
        print('oops')
    join_room(room)
    socketio.emit('group_response', json, room = room, callback=messageReceived)



if __name__ == '__main__':
    socketio.run(app,debug=True,port=5001)
