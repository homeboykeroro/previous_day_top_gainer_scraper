

import datetime
from constant.sqlite_query import SqliteQuery

def get_previous_day_top_gainer_list(connector, pct_change: float, start_date: datetime, end_date: datetime) -> bool:
    cursor = connector.cursor
    cursor.execute(SqliteQuery.GET_PREVIOUS_DAY_TOP_GAINER_QUERY.value, pct_change, (start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S')))
    
    rows = cursor.fetchall()
    return rows

def add_previous_day_gainer_record(connector, top_gainer_list: list):
    cursor = connector.cursor
    cursor.executemany(SqliteQuery.ADD_TOP_GAINER_QUERY.value, top_gainer_list)
    cursor.connection.commit()
    
def delete_all_previous_day_gainer_record(connector) -> int:
    cursor = connector.cursor
    cursor.execute(SqliteQuery.DELETE_ALL_TOP_GAINER_QUERY.value)
    cursor.connection.commit()
    return cursor.rowcount