import requests, json, glob, os
from datetime import datetime

## Time format transferring
def iso_time_formatter(*timestamps):
    formatted_dates = []
    for timestamp in timestamps:
        # Check if timestamp ends with 'Z' (UTC time)
        if timestamp.endswith('Z'):
            # Parse as UTC and convert to local time
            formatted_date = datetime.fromisoformat(timestamp.rstrip('Z')).isoformat()
        else:
            # Directly parse and format
            formatted_date = datetime.fromisoformat(timestamp).isoformat()
        formatted_dates.append(formatted_date)
    return formatted_dates

## Get current date information
def get_date_str(date, format):
    return date.strftime(format)

## Get IQAir weather and AQI information with API
def get_iqair_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            DATE_FORMAT = "%Y%m%d-%H%M%S"
            NOW = datetime.now()
            file_path = '/home/azureuser/tg_project/iqair_database/{now}.json'.format(now=get_date_str(NOW, DATE_FORMAT))
            
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

            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"JSON data successfully written to {file_path}")

            return city, pt, wt, aqi, mp, tp, hu, pr, ws

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

## Write down weather and AQI information into Notion
def write_to_notion(url, token, database_id, properties):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Successfully added entry to the database.")
        print(response.json())  # Prints the new page (entry) details
    else:
        print("Failed to add entry to the database.")
        print(response.status_code)
        print(response.text)

def find_aqi_from_json(root_dir, date):
    date_str = date.strftime("%Y%m%d")  # Format the date as 'YYYYMMDD'
    AQI = []

    # Search for files that match the pattern (including in subdirectories)
    for file_path in glob.glob(os.path.join(root_dir, '**', date_str + '-*.json'), recursive=True):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                # Navigate through the nested dictionaries to get to 'aqius'
                aqius_value = data.get('data', {}).get('current', {}).get('pollution', {}).get('aqius')
                if aqius_value is not None:
                    AQI.append(aqius_value)
            except json.JSONDecodeError as e:
                print(f"Error reading JSON file: {file_path}. Error: {e}")

    return AQI