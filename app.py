from flask import Flask, render_template, request, redirect, url_for, session
from message_func import get_user, add_user, chat_list
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
        if new_pass == '':
            error = 'Enter a password'
            return render_template('signup.html',error=error)
        if new_pass != confirm:
            error = 'Passwords do not match'
            return render_template('signup.html',error=error)
        add_user(new_log,new_pass)
        session['login'] = new_log
        return redirect('/chats')
    return render_template('signup.html')

@app.route('/chats', methods=['GET','POST'])
def chatting():
    return render_template('messaging.html', login = session['login'])

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)



if __name__ == '__main__':
    socketio.run(app,port=5001)
