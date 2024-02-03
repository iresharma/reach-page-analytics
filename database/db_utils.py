from datetime import datetime, timedelta

from typing import Tuple


def get_time_delta(time_delta: str) -> Tuple[float, float]:
    now = datetime.now()
    if time_delta == "YEAR":
        end = now - timedelta(days=365)
        return (now.timestamp(), end.timestamp())
    if time_delta == "MONTH":
        end = now - timedelta(days=28)
        return (now.timestamp(), end.timestamp())
    if time_delta == "WEEK":
        end = now - timedelta(days=7)
        return now.timestamp(), end.timestamp()
    if time_delta == "DAY":
        end = now - timedelta(hours=23)
        return end.timestamp(), now.timestamp()

