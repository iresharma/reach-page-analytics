from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS

from utils import get_ip_info
from database import add_view, add_click, calculate_unique_views, calculate_unique_clicks, calculate_ctr

load_dotenv()

app = Flask(__name__)
CORS(app)

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
    page_id = request.args.get('page')
    user_agent = request.headers.get('User-Agent')
    ip = request.remote_addr
    ip_info = get_ip_info(ip)
    add_view(page_id, user_agent, ip, ip_info)
    return 'OK'

@app.route('/clicks')
def index_clicks():
    """
    This reads the views we receive on the page, this accounts for both normal and unique
    :param:
        page-route  -> the page route
        input-ip    -> the IP address of the user
        user-agent  -> user agent of the user
    :return: OK
    """
    page_id = request.args.get('page')
    link_id = request.args.get('link')
    user_agent = request.headers.get('User-Agent')
    ip = request.remote_addr
    ip_info = get_ip_info(ip)
    add_click(page_id, link_id, user_agent, ip, ip_info)
    return 'OK'

@app.route('/views/unique')
def get_unique_views():
    """
    :param:
        page -> route of the page
    :return:
        unique_views -> <number>
    """
    page_id = request.headers.get('page-route')
    time_delta = request.args.get('time-delta')
    return calculate_unique_views(page_id, time_delta)

@app.route('/clicks/unique')
def get_unique_clicks():
    """
    :param:
        page -> route of the page
    :return:
        unique_views -> <number>
    """
    page_id = request.args.get('page')
    time_delta = request.args.get('time-delta')
    return calculate_unique_clicks(page_id, time_delta)

@app.route('/ctr')
def get_ctr():
    """
    :param:
    page-id -> number of unique views on a page
    :return:
    ctr -> <number>
    """
    page_route = request.args.get('page-route')
    time_delta = request.args.get('time-delta')
    return calculate_ctr(page_route, time_delta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4050, debug=True)
