# Previous Day Top Gainer Scraper

 <br />

### Core Dependencies
|Dependency|Description|
|:---------|:----------|
| beautifulsoup4 | Parsing HTML and XML documents |
| python-oracledb | Oracle database connection | 

 <br />

### Pre-Requisite
1. Install Oracle database
2. Execute `create.sql`
3. Edit `config.ini`, change Oracle login credentials and logger file directory

 <br />

### Local Debug Setup

1. Run `py -m venv VENV_NAME` to create project virtual environment
2. Go to venv directory, then execute `activate`
3. Run `pip install -r requirements.txt` to install dependencies
4. Debug in your IDE

 <br />

### Build Executable File
1. Run `pip install pyinstaller`
2. Run `pyinstaller main.py --icon=<icon_path>` to export this project as the executable file in `dist` folder 

 <br />

### Export Dependencies list
1. Run `pip3 freeze > requirements.txt`

<br />

### What It Does
Scrape information (ticker symbol, close and volume, etc.) of top 20 U.S market gainers in previous day from Finviz

<br />

### Schedule Job Setup For Automatic Execution (For Windows)
1. Open Windows task scheduler
2. Create task
3. Input criterion (Run daily at 4 a.m)
4.  Check "Run task as soon as possible after a scheduled start is missed" in Setting tab


