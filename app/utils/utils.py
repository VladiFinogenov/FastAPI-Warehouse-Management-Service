import logging

from sqlalchemy import event
from sqlalchemy.engine import Engine
import time

logger = logging.getLogger('my_logger')

# Инициализируем общий счетчик для SQL запросов
sql_query_count = 0

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    global sql_query_count
    sql_query_count += 1
    conn.info['start_time'] = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    start_time = conn.info.pop('start_time')
    elapsed_time = time.time() - start_time
    logger.info(f"SQL Query Count: {sql_query_count}, Elapsed Time: {elapsed_time:.4f}s, Query: {statement}")