from flask import Flask, render_template
from flask_apscheduler import APScheduler
import pyaudio
import numpy as np
import socket
import sys
import vlc

audio = pyaudio.PyAudio()
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

do_record = False
stream = None
sock = None

mp3Player = vlc.MediaPlayer("SubfolderForMicInputStuff/cmajorscale.mp3")
notPlayed = True

@app.route('/beforerec')
def beforerec():
    return render_template('recording.html', recording=False)

@app.route('/record')
def duringrec():
    global stream, do_record,sock

    stream = audio.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=1470)
    do_record = True

    # Establish socket connection to MATLAB
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 12346))

    return render_template('recording.html', recording=True, feedback="")

@app.route('/endrec')
def endrec():
    global do_record, stream, sock
    do_record = False 
    stream.stop_stream()
    stream.close()
    sock.close()

    return render_template('recording.html', recording=False)

def record():
    global do_record, stream, sock, notPlayed
    if do_record:
        data = stream.read(1470)
        try:
            sock.sendall(data)  # Send raw binary data
            if notPlayed:
                # mp3Player.play()
                notPlayed = False
            # sock.sendall(np.frombuffer(data, dtype=np.float32))
            # print(np.frombuffer(data, dtype=np.float32))  # Optional: print for debugging
            print(data)
        except ConnectionResetError:
            pass

if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.add_job(func=record, trigger="interval", id="job", seconds=0.033, max_instances=20)
    scheduler.start()
    app.run()
