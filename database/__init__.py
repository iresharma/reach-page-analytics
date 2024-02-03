from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import environ
from datetime import datetime
from certifi import where

from database.db_utils import get_time_delta

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


def calculate_unique_views(page: str, timeDelta: str):
    views_col = DB.views
    start, end = get_time_delta(timeDelta)
    print(start, end)
    vals = views_col.aggregate([
        {
            '$match': {
                'page_id': page,
                'timestamp': {
                    '$gte': end,
                    '$lte': start
                }
            }
        }, {
            '$group': {
                '_id': '$ip',
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$group': {
                '_id': None,
                'total_count': {
                    '$sum': '$count'
                }
            }
        }
    ])
    return list(vals)[0], 200


def calculate_unique_clicks(page: str, time_delta: str):
    clicks_col = DB.clicks
    start, end = get_time_delta(time_delta)
    print(start, end)
    vals = clicks_col.aggregate([
        {
            '$match': {
                'page_id': page,
                'timestamp': {
                    '$gte': end,
                    '$lte': start
                }
            }
        }, {
            '$group': {
                '_id': '$ip',
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$group': {
                '_id': None,
                'total_count': {
                    '$sum': '$count'
                }
            }
        }
    ])
    return list(vals)[0], 200


def calculate_ctr(page_id: str, time_delta: str):
    clicks_col = DB.clicks
    views_col = DB.views
    start, end = get_time_delta(time_delta)
    views_pipeline = [
        {
            "$match": {
                "page_id": page_id,
                "timestamp": {"$gte": end, "$lte": start}
            }
        },
        {
            "$group": {
                "_id": None,
                "viewsCount": {"$sum": 1}
            }
        }
    ]

    views_result = list(views_col.aggregate(views_pipeline, allowDiskUse=True))

    # Aggregate clicks
    clicks_pipeline = [
        {
            "$match": {
                "page_id": page_id,
                "timestamp": {"$gte": end, "$lte": start}
            }
        },
        {
            "$group": {
                "_id": None,
                "clicksCount": {"$sum": 1}
            }
        }
    ]

    clicks_result = list(clicks_col.aggregate(clicks_pipeline, allowDiskUse=True))

    views_count = views_result[0]["viewsCount"] if views_result else 0
    clicks_count = clicks_result[0]["clicksCount"] if clicks_result else 0

    ctr = clicks_count / views_count if views_count > 0 else 0
    return str(ctr * 100), 200

