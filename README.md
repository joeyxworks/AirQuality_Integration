# Weather and AQI Data Retrieval and Distribution

## Overview
This repository contains scripts for retrieving real-time weather and Air Quality Index (AQI) data from external sources such as IQAir. The data is then processed and distributed to various platforms including databases like Notion and social media platforms like Telegram.

## Features
- **Data Retrieval:** Fetches real-time weather and AQI data from IQAir.
- **Data Processing:** Processes the retrieved data for compatibility with various platforms.
- **Integration with Notion:** Automatically updates specified Notion databases with the latest data.
- **Telegram Bot Integration:** Sends updates to a designated Telegram bot with webhook.

## Getting Started

### Prerequisites
- Python 3.10.12 (In this case)
- API keys for IQAir
- Access tokens for Notion and Telegram Bot

### Configuration
- Add your API keys and access tokens with environment variables.
- Configure the target Notion database and Telegram channel/group IDs.

### Executing
- Run the script with a cron task or run as a system service according to your requirements.

### Tips
- Don't forget to connect your Notion API with your Notion Database.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
- IQAir for providing weather and AQI data.
- Notion and Telegram for their APIs.