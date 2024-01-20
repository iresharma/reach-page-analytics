from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import environ
from datetime import datetime
from certifi import where

uri = environ.get('MONGO_URI')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tls=True, tlsCAFile=where())
DB = client['reach-page-analytics']


def add_view(page: str, user_agent: str, ip: str, ip_info: dict):
    views_col = DB.views
    return views_col.insert_one(
        {
            "page_id": page,
            "timestamp": datetime.now().timestamp(),
            "user-agent": user_agent,
            "ip": ip,
            "ip_info": ip_info
        }
    ).inserted_id


def add_click(page: str, link: str, user_agent: str, ip: str, ip_info: dict):
    clicks_col = DB.clicks
    return clicks_col.insert_one(
        {
            "page_id": page,
            "timestamp": datetime.now().timestamp(),
            "user-agent": user_agent,
            "ip": ip,
            "ip_info": ip_info,
            "link": link
        }
    ).inserted_id


def calculate_unique_views(page: str):
    views_col = DB.views
    return views_col.find({"page_id": page}).distinct("ip")

def calculate_unique_clicks(page: str, link: str):
    clicks_col = DB.clicks
    return clicks_col.find({"page_id": page, "link": link}).distinct("ip")

def calculate_ctr(page: str):
    clicks_col = DB.clicks
    views_col = DB.views
    sum_of_clicks = clicks_col.find({ "page_id": page }).count()
    sum_of_views = views_col.find({ "page_id": page }).count()
    return (sum_of_clicks/sum_of_views)*100