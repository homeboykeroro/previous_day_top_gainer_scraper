

import datetime
from constant.sqlite_query import SqliteQuery

def check_if_previous_day_gainer_added(connector, ticker: str, scan_date: datetime):
    cursor = connector.cursor
    cursor.execute(SqliteQuery.CHECK_IF_PREVIOUS_GAINER_ADDED_QUERY.value, (ticker, scan_date.strftime('%Y-%m-%d')))
    
    result = cursor.fetchone()
    
    if result:
        if result[0]:
            return True
        else:
            return False
    else:
        return False
    
def add_previous_day_gainer_record(connector, top_gainer_list: list):
    cursor = connector.cursor
    cursor.executemany(SqliteQuery.ADD_TOP_GAINER_QUERY.value, top_gainer_list)
    cursor.connection.commit()
    
def delete_all_previous_day_gainer_record(connector) -> int:
    cursor = connector.cursor
    cursor.execute(SqliteQuery.DELETE_ALL_TOP_GAINER_QUERY.value)
    cursor.connection.commit()
    return cursor.rowcount