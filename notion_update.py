import requests
import os
from datetime import datetime
from library import get_date_str, get_iqair_data, write_to_notion

## Environment variables and URLs
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('NOTION_DB_ID')
iqair_key = os.getenv('KEY')
iqair_url = f'https://api.airvisual.com/v2/city?city=Shanghai&state=Shanghai&country=China&key={iqair_key}'
NOTION_API_URL = 'https://api.notion.com/v1/pages'

if __name__ == '__main__':
    result = get_iqair_data(iqair_url)
    
    if result:
        city, pt, wt, aqi, mp, tp, hu, pr, ws = result
        DATE_FORMAT = "%Y%m%d-%H%M"
        NOW = datetime.now()
        properties = {
            "Update": {"title": [{"text": {"content": get_date_str(NOW, DATE_FORMAT)}}]},
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

        write_to_notion(NOTION_API_URL, NOTION_TOKEN, DATABASE_ID, properties)
    
    else:
        print("Error retrieving data from IQAir.")



    
   