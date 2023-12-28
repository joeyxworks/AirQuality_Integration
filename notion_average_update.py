import requests
import os
import json
from datetime import datetime, timedelta
from library import get_date_str, get_iqair_data, write_to_notion, find_aqi_from_json

## Environment variables and URLs
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
ADATABASE_ID = os.getenv('NOTION_ADB_ID')
iqair_key = os.getenv('KEY')
iqair_url = f'https://api.airvisual.com/v2/city?city=Shanghai&state=Shanghai&country=China&key={iqair_key}'
NOTION_API_URL = 'https://api.notion.com/v1/pages'
DATE_FORMAT = "%Y%m%d"

today = datetime.now()
yesterday = today - timedelta(days=1)
today_date = today.date().isoformat()
yesterday_date = yesterday.date().isoformat()
root_dir = 'iqair_database/'

if __name__ == '__main__':
    AQI = find_aqi_from_json(root_dir, yesterday)
    average_aqi_yesterday = sum(AQI) / len(AQI)
    #print(average_aqi_yesterday)

    properties = {
        "Update": {"title": [{"text": {"content": get_date_str(today, DATE_FORMAT)}}]},
        "City": {"select": {"name": 'Shanghai'}},  # City as a select property
        "Date": {"date": {"start": yesterday_date}},
        "Average AQI": {"number": average_aqi_yesterday},
    }

    write_to_notion(NOTION_API_URL, NOTION_TOKEN, ADATABASE_ID, properties)