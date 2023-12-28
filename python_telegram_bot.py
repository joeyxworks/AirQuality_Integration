import logging, os, requests, json, pytz
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

iqair_key = os.environ['KEY']
iqair_url = 'https://api.airvisual.com/v2/city?city=Shanghai&state=Shanghai&country=China&key={KEY}'.format(KEY=iqair_key)


## Retrieve data with IQ Air API
async def get_iqair_data(url):
    response = requests.get(url)
    data = response.json()

    current_data = data['data']['current']
    pollution_data = current_data['pollution']
    weather_data = current_data['weather']
    city_value = data['data']['city']

    return {
        'pollution_data': pollution_data,
        'weather_data': weather_data,
        'city': city_value
    }

## Adjust time stamp format and time zone
def iso_time_formatter(*iso_time_strs):
    formatted_times = []

    utc_zone = pytz.utc
    cst_zone = pytz.timezone('Asia/Shanghai')  # GMT+8 timezone

    for iso_time_str in iso_time_strs:
        iso_time_str = iso_time_str.replace('Z', '')
        dt_obj_utc = datetime.fromisoformat(iso_time_str).replace(tzinfo=utc_zone)
        dt_obj_cst = dt_obj_utc.astimezone(cst_zone)
        readable_time_str = dt_obj_cst.strftime("%Y/%m/%d %I:%M %p")
        formatted_times.append(readable_time_str)
    return formatted_times

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


## Respond messages sent from users with Telegram Bot API
## For command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )

## For command /weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    iqair_data = await get_iqair_data(iqair_url)

    aqius_value = iqair_data['pollution_data']['aqius']
    mainus_value = iqair_data['pollution_data']['mainus']
    temperature_value = iqair_data['weather_data']['tp']
    humidity_value = iqair_data['weather_data']['hu']
    pr_value = iqair_data['weather_data']['pr']
    ws_value = iqair_data['weather_data']['ws']
    city_value = iqair_data['city']
    pollution_ts = iqair_data['pollution_data']['ts']
    weather_ts = iqair_data['weather_data']['ts']
    formatted_pollution_ts, formatted_weather_ts = iso_time_formatter(pollution_ts, weather_ts)

    message_text = (
        # "Here's today's weather information for {city}:\n\n"
        # "*AQI:* {aqi} (Time: {pt})\n"
        # "*Temperature:* {tp}°C (Time: {wt})\n"
        # "*Humidity:* {hu}% (Time: {wt})"

        "Current weather information for *{city}*:\n\n"
        "Pollution (Updated: {pt}):\n"
        "- *AQI*: {aqi}\n"
        "- *Main pollutant*: {mp}\n\n"
        "Weather (Updated: {wt}):\n"
        "- *Temperature*: {tp}°C\n"
        "- *Humidity*: {hu}%\n"
        "- *Atmospheric pressure*: {pr} hPa\n"
        "- *Wind speed*: {ws} (m/s)"
    ).format(
        city=city_value,
        aqi=aqius_value,
        mp=mainus_value,
        tp=temperature_value,
        hu=humidity_value,
        pt=formatted_pollution_ts,
        wt=formatted_weather_ts,
        pr=pr_value,
        ws=ws_value,
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text,
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ['TOKEN']).build()
    
    start_handler = CommandHandler('start', start)
    weather_handler = CommandHandler('weather', weather)
    application.add_handler(start_handler)
    application.add_handler(weather_handler)
    
    application.run_polling()