from flask import *
import requests
import json

app = Flask(__name__)


received_data = {}

@app.route('/receive_data', methods=['POST'])
def receive_data():
    global received_data
    try:
        received_data = request.json
        return jsonify({'status': 'success', 'received_data': received_data})
    except Exception as e:
        app.logger.error(f"Error receiving data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(received_data)
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/game')
def game():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)
