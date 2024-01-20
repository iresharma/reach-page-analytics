from flask import Flask, request
from dotenv import load_dotenv
from utils import get_ip_info
from database import add_view, add_click, calculate_unique_views, calculate_unique_clicks, calculate_ctr

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
    print(page_id)
    return calculate_unique_views(page_id)

@app.route('/clicks/unique')
def get_unique_clicks():
    """
    :param:
        page -> route of the page
    :return:
        unique_views -> <number>
    """
    page_id = request.args.get('page')
    link_id = request.args.get('link')
    return calculate_unique_clicks(page_id, link_id)

@app.route('/ctr')
def get_ctr():
    """
    :param:
    page-id -> number of unique views on a page
    :return:
    ctr -> <number>
    """
    page_id = request.args.get('page')
    return calculate_ctr(page_id)

if __name__ == '__main__':
    app.run(debug=True)
