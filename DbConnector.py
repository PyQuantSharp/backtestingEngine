import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


class DbConnector:
    def __init__(self):
        self.db = None

    def connect(self):
        self.db = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user="root",
            # passwd=os.getenv('DB_PASSWORD'),
        )
        return self.db


if __name__ == '__main__':
    db = DbConnector()
    db.connect()
