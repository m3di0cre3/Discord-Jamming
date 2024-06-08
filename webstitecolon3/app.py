from flask import *
from flask_apscheduler import APScheduler
import requests
import json

app = Flask(__name__)

counter = 0
received_data = "loading!"

def get_data():
    global counter
    counter += 1
    return str(counter)

# buttons ish
@app.route('/')
def index():
    counter = get_data()
    return render_template('index.html',counter=counter)

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
    scheduler = APScheduler()
    scheduler.add_job(func=get_data,trigger='interval',id='job',seconds = 1)
    scheduler.start()
    app.run(debug=True)
