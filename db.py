"""
The database layer, extracted away.
"""
import json
import mysql.connector
from mysql.connector import errorcode
from contextlib import closing

class DatabaseError(Exception):
    pass

def getCredentials():
    # Returns username, password, connection string info - is this a bad idea?
    data = None
    with open('config.json', 'r') as f:
        data = json.load(f)['db']
    return data

def getConnection():
    config = getCredentials()
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connctor.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong username/password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def runQuery(query):
    credentials = getCredentials()
    with closing(mysql.connector.connect(**credentials)) as conn:
        with closing(conn.cursor(buffered=True)) as cursor:
            cursor.execute(query)
            return cursor.fetchall().copy()

def runScalarQuery(query):
    try:
        return runQueryThree(query)[0][0]
    except IndexError as e:
        return None

def runUpdateQuery(query):
    credentials = getCredentials()
    with closing(mysql.connector.connect(**credentials)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query)
            conn.commit()
            return cursor.lastrowid

def testConnection():
    results = runQuery("SELECT 1")
    assert results[0][0] == 1

if __name__ == '__main__':
    testConnection()
