import oracledb

from sql.execute_query_impl import ExecuteQueryImpl

from utils.config_util import get_config
from utils.logger import Logger

logger = Logger()

HOSTNAME = get_config('ORACLE_DB', 'HOSTNAME')
PORT = get_config('ORACLE_DB', 'PORT')
SID = get_config('ORACLE_DB', 'SID')
USERNAME = get_config('ORACLE_DB', 'USERNAME')
PASSWORD = get_config('ORACLE_DB', 'PASSWORD')

MIN_CONNECTION_IN_POOL = get_config('ORACLE_DB', 'MIN_CONNECTION_IN_POOL')
MAX_CONNECTION_IN_POOL = get_config('ORACLE_DB', 'MAX_CONNECTION_IN_POOL')
POOL_CONNECTION_INCREMENT = get_config('ORACLE_DB', 'POOL_CONNECTION_INCREMENT')

LOGIN_CREDENTIALS = dict(host=HOSTNAME, 
                        port=PORT, 
                        sid=SID,
                        user=USERNAME, 
                        password=PASSWORD,
                        min=MIN_CONNECTION_IN_POOL,
                        max=MAX_CONNECTION_IN_POOL,
                        increment=POOL_CONNECTION_INCREMENT)

pool = oracledb.create_pool(**LOGIN_CREDENTIALS)

def execute_in_transaction(execute_query: ExecuteQueryImpl, params):
    connection = None
    cursor = None
    
    result = None
    
    try:
        connection = pool.acquire()
        cursor = connection.cursor()
        
        result = execute_query.execute(cursor, params)
        
        connection.commit()
    except oracledb.Error as e:
        connection.rollback()
        logger.log_error_msg(f'Oracle SQL error, {e}')
        raise e
    finally:
        if pool is not None:
            if connection is not None:
                if cursor is not None:
                    cursor.close()

                pool.release(connection)
        
    return result
