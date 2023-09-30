import os
from dotenv import load_dotenv
import mysql.connector.pooling
import redis

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
    decode_responses=True,
)
ACCESS_SECRET = os.getenv("JWT_ACCESS_SECRET")
REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET")
