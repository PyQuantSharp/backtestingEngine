import os
import string
import regex as re
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()


def cleanFile(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        new_lines = []
    for line in lines:
        new_line = line
        if "0expiry" in line:
            new_line = new_line.replace("0expiry", "0\nexpiry")
        if re.match("[A-Z]", new_line.split(",")[0]) or line.split(",")[0] == "":
            new_line = None
        if new_line:
            new_lines.append(new_line)

    with open(filepath, "w") as f:
        f.writelines(new_lines)


def genOptionNames(filepath):
    df = pd.read_csv(filepath)
    df["symbol"] = df["symbol"].apply(lambda x: x.upper().split(" ")[0]) + pd.to_datetime(df['expiry']).apply(
        lambda x: x.strftime("%y%m%d")) + df["type"].replace("Call", "C").replace("Put", "P") + df["strike"].astype(str)
    df.to_csv(filepath, index=False)


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

    def getTable(self, table_name: string) -> pd.DataFrame:
        query = "SELECT * FROM " + table_name
        df = pd.read_sql(query, self.cnx)
        return df


if __name__ == '__main__':
    db = DbConnector()
    # db.csv_to_db('./exampleData/spy_options_eod.csv')
    # cleanFile('./exampleData/spy_options_eod.csv')
    genOptionNames('./exampleData/spy_options_eod.csv')
