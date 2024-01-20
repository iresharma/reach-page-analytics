from json import loads

from ip2geotools.databases.noncommercial import DbIpCity

def get_ip_info(ip: str):
    res = DbIpCity.get(ip, api_key="free")
    return loads(res.to_json())