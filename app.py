import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

socketio = SocketIO(app,logger=True, engineio_logger=True,cors_allowed_origins="*" ,manage_session=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method=='POST'):
        username = request.json['username']
        room = request.json['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
    return render_template("none.html",session=session)
@socketio.on('join')
def join(message):
    join_room(message["room"])
    emit('status', {'msg': message["username"] + ' has entered the room.',"sentByMe":message["sentByMe"]}, room=message["room"])
@socketio.on('text')
def text(message):
    room = str(message['room'])
    join_room(message["room"])
    emit('message', {'msg': message['username'] + ' : ' + message['msg'],"sentByMe":message['sentByMe']}, room=message["room"])
@socketio.on('image')
def image(message):
    room = str(message['room'])
    emit('imagesend',{'msg':'img',"img":message['img'],"sentByMe":message['sentByMe']}, room=message["room"])
@socketio.on('video')
def video(message):
    room = str(message['room'])
    emit('videosend',{'msg':'video',"video":message['video'],'sentByMe':message['sentByMe']},room = message["room"])
if __name__ == '__main__':
    socketio.run(app,debug=False)
