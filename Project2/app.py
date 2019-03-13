from flask import Flask, render_template

app = Flask(__name__)

from content_management import Content

TOPIC_DICT = Content()
@app.route('/')
def hello_world():
    return render_template('dashboard.html', title='Log in',TOPIC_DICT = TOPIC_DICT)


if __name__ == '__main__':
    app.run()
