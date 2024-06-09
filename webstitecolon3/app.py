from flask import *
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO,emit
from random import choice
import requests
import base64
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret!'
socketio = SocketIO(app)

counter = 0
received_data = "loading!"

def get_music_feedback_from_music():
    return choice(['good','great','awesome','fantastic','bad','horrible','terrible','complete trash'])
lyrics = {0:'i',1:'wanna',2:'eat',3:'something'}
piano_notes = ['A','B','C','D','E','F','G','H','I']
cur_lyric_index = 0
cur_piano_index = 0

@app.route('/choose_song', methods=['GET'])
def choose_song_menu():
    query = request.args.get('query')
    return render_template('choose_song.html')

def get_music_feedback():
    socketio.emit("music_feedback",{"data":get_music_feedback_from_music()})

def get_lyrics():
    global lyrics
    global cur_lyric_index
    cur_lyric_index += 1
    if cur_lyric_index == 4:
        cur_lyric_index = 0
    socketio.emit("lyric",{"data":lyrics[cur_lyric_index]})

def get_piano_note():
    global piano_notes
    global cur_piano_index
    if cur_piano_index < len(piano_notes)-1:
        cur_piano_index += 1
    socketio.emit("piano_note",{"data":piano_notes[cur_piano_index]})

# buttons ish
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play_menu')
def play_game_menu():
    return render_template('play_menu.html')

@app.route('/play_menu/vocal_game')
def vocal_game():
    return render_template('vocal_game.html')

@app.route('/play_menu/guitar_game')
def guitar_game():
    return render_template('guitar_game.html')

@app.route('/play_menu/piano_game')
def piano_game():
    return render_template('piano_game.html')
@app.route('/play_menu/end_screen')
def end_game():
    return render_template('end_screen.html')


# progress code
song = 'green'

@app.route('/receive_progress', methods=['POST'])
def receive_progress():
    global received_data
    try:
        received_data = request.json
        return jsonify({'status': 'success', 'received_progress': received_data})
    except Exception as e:
        app.logger.error(f"Error receiving data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/get_progress', methods=['GET'])
def get_progress():
    return jsonify(received_data)

# song code

@app.route('/receive_song', methods=['POST'])
def receive_song():
    global song
    try:
        song = request.json
        return jsonify({'status': 'success', 'received_song': song})
    except Exception as e:
        app.logger.error(f"Error receiving data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_song', methods=['GET'])
def get_song():
    return jsonify(song)

# jfdklf
if __name__ == '__main__':
    counter += 1
    scheduler = APScheduler()
    scheduler.add_job(func=get_music_feedback,trigger='interval',id='job',seconds = 1)
    scheduler.add_job(func=get_lyrics,trigger='interval',id='job2',seconds = 1)
    scheduler.add_job(func=get_piano_note,trigger='interval',id='jo32',seconds = 1)
    scheduler.start()
    app.run(debug=True)
