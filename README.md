# Previous Day Top Gainer Scraper

 <br />

### Core Dependencies
|Dependency|Description|
|:---------|:----------|
| beautifulsoup4 | Parsing HTML and XML documents |
| discord\.py | Sending message to discord server |
| python-oracledb | Oracle database connection | 

 <br />

### Pre-Requisite
1. Install Oracle database
2. Execute `create.sql`
3. Edit `config.ini`, change Oracle login credentials and logger file directory
4. Create discord account and server, [set up your discord chatbot](https://streamlabs.com/content-hub/post/connecting-chatbot-to-discord-desktop-chatbot)
5. Create environment variables using this command: 
```
SET
DISCORD_CHATBOT_TOKEN=<your_chatbot_token>
DISCORD_TEXT_TO_SPEECH_CHANNEL_ID=<the_channel_id_for_text_to_speech>
DISCORD_YESTERDAY_TOP_GAINER_SCRAPER_HISTORY_CHANNEL_ID=<the_channel_id_for_displaying_scraper_history>
CHATBOT_ERROR_LOG=<the_channel_id_for_displaying_error_log>
```

 <br />

### Local Debug Setup

1. Run `py -m venv VENV_NAME` to create project virtual environment
2. Go to venv directory, then execute `activate`
3. Run `pip install -r requirements.txt` to install dependencies
4. Debug in your IDE

 <br />

### Build Executable File
1. Run `pip install pyinstaller`
2. Run `pyinstaller main.spec` to export this project as the executable file in `dist` folder 

 <br />

### Export Dependencies list
1. Run `pip3 freeze > requirements.txt`

<br />

### What It Does
Scrape information (ticker symbol, close and volume, etc.) of top 20 U.S market gainers in previous day from Finviz. Notifications will be sent to discord server to confirm if data retrieval is succeeded or failed. The data will be analysed by [stock_scanner](https://github.com/homeboykeroro/stock_scanner/)

<img width="943" alt="finviz" src="https://github.com/homeboykeroro/previous_day_top_gainer_scraper/assets/85852490/8e34c0c1-bb07-452d-aeee-5a3d0724c98d">


<br />
<br />

