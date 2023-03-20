from crypt import methods

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/hello/')
def hello():
    return 'hahahahihi adsdas'


@app.route('/blog/<int:postID>', methods=['POST'])
def show_blog(postID):
    return 'Blog Number %d' % postID


# Chạy với hotreload: flask --app main.py --debug run
if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
