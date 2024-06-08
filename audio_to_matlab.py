from flask import Flask, render_template
from flask_apscheduler import APScheduler
import pyaudio
import numpy as nppip 
import socket

audio = pyaudio.PyAudio()
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

do_record = False
stream = None
sock = None

@app.route('/beforerec')
def beforerec():
    return render_template('recording.html', recording=False)

@app.route('/record')
def duringrec():
    global stream, do_record, sock

    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    do_record = True

    # Establish socket connection to MATLAB
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('localhost', 65432))

    return render_template('recording.html', recording=True, feedback="")

@app.route('/endrec')
def endrec():
    global do_record, stream, sock
    do_record = False 
    stream.stop_stream()
    stream.close()
    sock.close()

    return render_template('recording.html', recording=False)

@app.route('/get_feedback')
def get_feedback():
    global sock
    feedback = sock.recv(1024).decode('utf-8')
    return feedback
def record():
    global do_record, stream, sock
    if do_record:
        data = stream.read(1024)
        sock.sendall(data)  # Send audio data to MATLAB

        new_data = np.frombuffer(data, dtype=np.int16)
        print(new_data)

if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.add_job(func=record, trigger="interval", id="job", seconds=1, max_instances=1)
    scheduler.start()
    app.run()