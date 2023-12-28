import requests
import os
from datetime import datetime

## Time format transferring
def iso_time_formatter(pollution_ts, weather_ts):
    # Example implementation, adjust as needed
    pt = datetime.fromisoformat(pollution_ts.rstrip('Z')).isoformat()
    wt = datetime.fromisoformat(weather_ts.rstrip('Z')).isoformat()
    return pt, wt

## Environment variables and URLs
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('NOTION_DB_ID')
iqair_key = os.getenv('KEY')
iqair_url = f'https://api.airvisual.com/v2/city?city=Shanghai&state=Shanghai&country=China&key={iqair_key}'
NOTION_API_URL = 'https://api.notion.com/v1/pages'

## Get current date information
def get_today_with_counter():
    now = datetime.now()
    return now.strftime("%H%M%S%y%m%d")

## Get IQAir weather and AQI information with API
def get_iqair_data(url):
    response = requests.get(url)
    data = response.json()
    print(data)
    current_data = data['data']['current']
    pollution_data = current_data['pollution']
    weather_data = current_data['weather']

    aqi = pollution_data['aqius']
    mp = pollution_data['mainus']
    pollution_ts = pollution_data['ts']

    tp = weather_data['tp']
    hu = weather_data['hu']
    pr = weather_data['pr']
    ws = weather_data['ws']
    weather_ts = weather_data['ts']

    city = data['data']['city']
    pt, wt = iso_time_formatter(pollution_ts, weather_ts)

    return city, pt, wt, aqi, mp, tp, hu, pr, ws

## Write down weather and AQI information into Notion
def write_to_notion(url, token, database_id, city, pt, wt, aqi, mp, tp, hu, pr, ws):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Update": {"title": [{"text": {"content": get_today_with_counter()}}]},
            "City": {"select": {"name": city}},  # City as a select property
            "Pollution Updated": {"date": {"start": pt}},
            "AQI": {"number": aqi},
            "Main Pollutant": {"rich_text": [{"text": {"content": mp}}]},  # Assuming Main Pollutant is a rich_text property
            "Weather Updated": {"date": {"start": wt}},
            "Temperature (°C)": {"number": tp},
            "Humidity (%)": {"number": hu},
            "Wind Speed (m/s)": {"number": ws},
            "Pressure (hPa)": {"number": pr}
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Successfully added entry to the database.")
        print(response.json())  # Prints the new page (entry) details
    else:
        print("Failed to add entry to the database.")
        print(response.status_code)
        print(response.text)

if __name__ == '__main__':
    city, pt, wt, aqi, mp, tp, hu, pr, ws = get_iqair_data(iqair_url)
    write_to_notion(NOTION_API_URL, NOTION_TOKEN, DATABASE_ID, city, pt, wt, aqi, mp, tp, hu, pr, ws)