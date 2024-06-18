import sys
import os
from typing import Final
import MySQLdb
from dotenv import load_dotenv

load_dotenv()
DB: Final[str] = os.getenv("DATABASE")
DB_USERNAME: Final[str] = os.getenv("DATABASE_USERNAME")
DB_PW: Final[str] = os.getenv("DATABASE_PASSWORD")
DB_HOST: Final[str] = os.getenv("DATABASE_HOST")
DB_PORT: Final[str] = os.getenv("DATABASE_PORT")


print(f"DB: {DB}, DB_USERNAME: {DB_USERNAME}, PW: {DB_PW}, HOST: {DB_HOST}, PORT: {DB_PORT}")

# Connect to MariaDB Platform
try:
    conn = MySQLdb.connect(
        user=DB_USERNAME,
        password=DB_PW,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB
    )
except MySQLdb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()


def get_users():
    print('Ready to get users')
    try:
        query = '''
            SELECT username
            FROM users
        '''
        cur.execute(query)
        res = [username for (username,) in cur.fetchall()]
        return res
    except MySQLdb.Error as e:
        print(f"Error fetching users: {e}")
        return [] 

def insert_user(name: str):
    print(f'DB insert user: {name}')
    try:
        query = '''
            INSERT INTO users (username) VALUES (%s)
        '''
        cur.execute(query, (name,))
        conn.commit()
    except MySQLdb.Error as e:
        print(f"Error inserting user: {e}")


