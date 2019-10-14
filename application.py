from flask import Flask
app = Flask(__name__)

env = ''
env = 'DEVELOP'


@app.route('/')
def hello_world():
    return "Hello World!２"


@app.route('/api/<int:id>')
def api(id):
    return pose(id)


def pose(id):
    return "pose" * id


if __name__ == '__main__':
    if env == 'DEVELOP':
        app.debug = True
    app.run()
