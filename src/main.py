
import time
from bs4 import BeautifulSoup
import requests

from utils.datetime_util import get_current_us_datetime
from sql.previous_day_top_gainer_sql_util import add_previous_day_gainer_record
from sql.sqlite_connector import SqliteConnector

from utils.logger import Logger

FINVIZ_LINK = 'https://finviz.com/screener.ashx'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
TOP_GAINER_PAYLOAD = {'s': 'ta_topgainers'}

session = requests.Session()
logger = Logger()

def main():  
    sqlite_connector = SqliteConnector()
    scan_date = get_current_us_datetime().strftime('%Y-%m-%d')

    try:
        scrap_star_time = time.time()
        response = session.get(FINVIZ_LINK, params=TOP_GAINER_PAYLOAD, headers=HEADERS)
        logger.log_debug_msg(f'Scrap {FINVIZ_LINK} response time: {time.time() - scrap_star_time} seconds')
        # Raises a HTTPError if the response status is 4xx, 5xx
        response.raise_for_status() 
    except Exception as e:
        logger.log_error_msg(f'An error occurred while scarping data: {e}')
    else:
        top_gainer_list = []
        contents = response.text
        soup = BeautifulSoup(contents, 'lxml')
        row_list = soup.select('table.screener_table tr.styled-row')
    
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
                num = float(market_cap_str.replace(',', ''))
                market_cap = int(num * multiplier)
                
            top_gainer_list.append((ticker, company, 
                                    sector, industry,
                                    scan_date, 
                                    change_pct, volume, close_price,
                                    market_cap, country))

        add_previous_day_gainer_record(sqlite_connector, top_gainer_list)
        logger.log_debug_msg('Previous day top gainers scrap completed', with_std_out=True)
        
if __name__ == '__main__':
    main()
