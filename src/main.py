
import time
from bs4 import BeautifulSoup
import requests

from sql.previous_day_top_gainer_sql_util import add_previous_day_gainer_record, check_if_previous_day_gainer_added
from sql.sqlite_connector import SqliteConnector

from utils.text_to_speech_engine import TextToSpeechEngine
from utils.datetime_util import check_if_us_business_day, get_current_us_datetime

from utils.logger import Logger

FINVIZ_LINK = 'https://finviz.com/screener.ashx'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
TOP_GAINER_PAYLOAD = {'s': 'ta_topgainers'}

session = requests.Session()
logger = Logger()

text_to_speech_engine = TextToSpeechEngine()

EXIT_WAIT_TIME = 30

def main():  
    sqlite_connector = SqliteConnector()
    scan_date = get_current_us_datetime()
    is_business_day = check_if_us_business_day(scan_date)

    if not is_business_day:
        text_to_speech_engine.speak('No data is fetched, current datetime is not U S business day')
        logger.log_error_msg(f'No data is fetched, current datetime is not US business day', with_std_out=True)
        return
    
    try:
        scrap_star_time = time.time()
        response = session.get(FINVIZ_LINK, params=TOP_GAINER_PAYLOAD, headers=HEADERS)
        logger.log_debug_msg(f'Scrap {FINVIZ_LINK} response time: {time.time() - scrap_star_time} seconds', with_std_out=True)
        # Raises a HTTPError if the response status is 4xx, 5xx
        response.raise_for_status() 
    except Exception as e:
        logger.log_error_msg(f'An error occurred while scarping data: {e}', with_std_out=True)
    else:
        top_gainer_list = []
        contents = response.text
        soup = BeautifulSoup(contents, 'lxml')
        row_list = soup.select('table.screener_table tr.styled-row')

        try:
            for row in row_list:
                column_list = row.find_all('td')
                ticker = column_list[1].text
                company = column_list[2].text
                sector = column_list[3].text
                industry = column_list[4].text
                country = column_list[5].text
                market_cap_str = column_list[6].text
                close_price = float(column_list[8].text.replace(',', ''))
                change_pct = float(column_list[9].text.replace('%', ''))
                volume = int(column_list[10].text.replace(',', ''))

                market_cap = 0
                if market_cap_str:
                    multiplier = 1

                    if market_cap_str.endswith('K'):
                        multiplier = 1e4
                    if market_cap_str.endswith('M'):
                        multiplier = 1e6
                    elif market_cap_str.endswith('B'):
                        multiplier = 1e9

                    market_cap_str = market_cap_str[:-1]
                    num = float(market_cap_str.replace(',', '')) if market_cap_str else 0
                    market_cap = int(num * multiplier)

                is_gainer_added = check_if_previous_day_gainer_added(sqlite_connector, ticker, scan_date)  
                if not is_gainer_added:
                    top_gainer_list.append((ticker, company, 
                                            sector, industry,
                                            scan_date.strftime('%Y-%m-%d'), 
                                            change_pct, volume, close_price,
                                            market_cap, country))

            add_previous_day_gainer_record(sqlite_connector, top_gainer_list)
        except Exception as e:
            text_to_speech_engine.speak('Previous day top gainer history retrieval failed')
            logger.log_error_msg(f'Error occurs: {e}')
            time.sleep(EXIT_WAIT_TIME)
        
        text_to_speech_engine.speak('Previous day top gainer history retrieval succeed')
        logger.log_debug_msg('Previous day top gainers scrap completed', with_std_out=True)
        
if __name__ == '__main__':
    main()