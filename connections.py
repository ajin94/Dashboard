import MySQLdb

DATABASE_MAP = {
    'NSI': 'nsinteriors',
    'SF': 'shadowfashion',
    'DASH': 'dashboard'
}


def get_connection_to(db_name='dash'):
    conn = MySQLdb.connect(host="localhost", user="root", passwd="sh@d0w", port=3306, db=DATABASE_MAP[db_name.upper()])
    # conn = MySQLdb.connect(host="localhost", user="root", passwd="password", port=3306, db=DATABASE_MAP[db_name.upper()])
    cursor = conn.cursor()
    return cursor, conn

