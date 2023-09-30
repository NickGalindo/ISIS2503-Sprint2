import os
from dotenv import load_dotenv
import mysql.connector.pooling
import redis
from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def __getPasswordHash(password):
    return PWD_CONTEXT.hash(password)

load_dotenv()

mysqlConnectionPool = mysql.connector.pooling.MySQLConnectionPool(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    pool_name="auth-pooling",
    pool_size=10,
)
redisConnectionPool = redis.ConnectionPool(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    decoded_response=True,
)
ACCESS_SECRET = os.getenv("JWT_ACCESS_SECRET")
REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET")


__db = mysqlConnectionPool.get_connection()
__cursor = __db.cursor()

q = """
INSERT INTO auth.users (name, email, password_hashed, password_salt, state)
VALUES
"""

for i in range(50):
    q = q + f"('User{i}', 'user{i}@wubbalubbadubdub.com', '{__getPasswordHash('123456')}', 'salt{i}', 'active')"
    if i == 49:
        q = q + ';'
    else:
        q = q + ',\n'

__cursor.execute(q)

__db.commit()
__cursor.close()
__db.close()
