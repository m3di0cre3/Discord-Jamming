import flask as fl

app = fl.Flask(__name__)

@app.route('/')
def index():
    return fl.render_template('index.html')

@app.route('/about')
def about():
    return fl.render_template('about.html')

@app.route('/game')
def game():
    return fl.render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)
