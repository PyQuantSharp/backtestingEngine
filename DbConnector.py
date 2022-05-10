import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()


class DbConnector:
    def __init__(self):
        self.cnx = None
        self._connect()

    def _connect(self):
        self.cnx = create_engine('mysql+pymysql://root:@localhost:3306/financialdata', echo=False)

    def csv_to_db(self, csv_path):
        df = pd.read_csv(csv_path)
        file_name = os.path.basename(csv_path).replace('.csv', '').lower()
        df.to_sql(name=file_name, con=self.cnx, if_exists='replace', index=False)

    def getSet(self, dataset):
        query = "SELECT * FROM " + dataset
        df = pd.read_sql(query, self.cnx)
        return df


if __name__ == '__main__':
    db = DbConnector()
    db.csv_to_db('./exampleData/spy_options_eod.csv')
