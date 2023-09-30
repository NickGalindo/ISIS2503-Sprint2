import mysql.connector
from authentication import mysqlConnectionPool as pool
from colorama import Fore

def dbQuery(query: str):
    __db = pool.get_connection()
    __cursor = __db.cursor()
    try:
        __cursor.execute(query)
    except Exception as e:
        print(Fore.RED + f"ERROR: query failed")
        print(e)
        
        __cursor.close()
        __db.close()
        
        return None

    data = __cursor.fetchall()

    __cursor.close()
    __db.close()

    return data

def dbUpdate(upd: str):
    __db = pool.get_connection()
    __cursor = __db.cursor()
    try:
        __cursor.execute(upd)
    except Exception as e:
        print(Fore.RED + f"ERROR: update failed")
        print(e)
        
        __cursor.close()
        __db.close()

    __db.commit()
    __cursor.close()
    __db.close()
