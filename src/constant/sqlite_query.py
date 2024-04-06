from enum import Enum

class SqliteQuery(str, Enum):
    ADD_TOP_GAINER_QUERY = "INSERT INTO top_gainer_history VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    DELETE_ALL_TOP_GAINER_QUERY = "DELETE FROM top_gainer_history"
    GET_PREVIOUS_DAY_TOP_GAINER_QUERY = 'SELECT * FROM top_gainer_history WHERE percentage >= ? AND scan_date >= ? AND scan_date <= ?'
    CHECK_IF_PREVIOUS_GAINER_ADDED_QUERY = 'SELECT EXISTS (SELECT 1 FROM top_gainer_history WHERE ticker = ? AND scan_date = ?)'