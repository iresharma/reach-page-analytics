from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Tracking analytics for all your beautiful pages'

@app.route('/views')
def index_views():
    """
    This reads the views we receive on the page, this accounts for both normal and unique
    :param:
        page-route -> the page route
        input-ip -> the IP address of the user
        user-agent -> user agent of the user
    :return: OK
    """
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    return 'OK'


if __name__ == '__main__':
    app.run()
