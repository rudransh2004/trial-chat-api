from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

socketio = SocketIO(app,logger=True, engineio_logger=True,cors_allowed_origins="*" ,manage_session=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method=='POST'):
        username = request.json['username']
        room = request.json['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        print(session.get('username'))
        print(session.get('room'))
     return render_template("none.html",session=session)
@socketio.on('join')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)
@socketio.on('text')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)
if __name__ == '__main__':
    socketio.run(app,debug=False)
