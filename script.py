import requests
import mysql.connector
import decimal
import logging
import pandas as pd
import warnings
import sys
from inputimeout import inputimeout, TimeoutOccurred

class BankAPI:
    def __init__(self):
        #get usd response as json
        self.table_usd = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json").json()
        #get eur response as json
        self.table_eur = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json").json()


    #function to return current usd price
    def get_usd(self):
        usd = self.table_usd['rates'][0]['mid']
        return usd


    #function to return current eur price
    def get_eur(self):
        eur = self.table_eur['rates'][0]['mid']
        return eur


class ConnectSQL:
    def __init__(self, usernme, passwrd, databse):
        #connection with database
        self.conn = mysql.connector.connect(user=usernme, password=passwrd,
                                            host="127.0.0.1", database=databse)
        #set cursor
        self.cursor = self.conn.cursor()
    

    def execute(self, comm):
        self.cursor.execute(comm)


    def commit(self):
        self.conn.commit()


    # disconnect
    def close(self):
        self.conn.close()

def get_excel(sql):
    get_data = "SELECT ProductID, DepartmentID,\
                Category, IDSKU, ProductName,\
                Quantity, UnitPrice, UnitPriceUSD,\
                UnitPriceEuro, Ranking, ProductDesc,\
                UnitsInStock, UnitsInOrder FROM mydb.product;"
    
    sql_query = pd.read_sql(get_data, sql.conn)
    print("Created excel table.")
    logging.debug("Created excel table.")
    sql_query.to_excel('productTable.xlsx')

if __name__=="__main__":
    logging.basicConfig(filename='script.log', level=logging.DEBUG,
                        format = '%(asctime)s:%(message)s')
    warnings.filterwarnings(action='ignore', category=UserWarning)

    try:
        nbp = BankAPI()
        usd_now = decimal.Decimal(nbp.get_usd())
        eur_now = decimal.Decimal(nbp.get_eur())
    except:
        logging.exception("Error NBP:")
        raise
    
    try:
        sql = ConnectSQL("root", "zaq1@WSX", "mydb")
    except:
        logging.exception("Error SQL:")
        raise
    else:
        upd = f"UPDATE mydb.product SET UnitPriceUSD = UnitPrice/{usd_now}, UnitPriceEuro = UnitPrice/{eur_now};"
        sql.execute(upd)
        sql.commit()
        try:
            something = inputimeout(prompt="Click enter to create excel file." , timeout=5)
        except TimeoutOccurred:
            sys.exit()
        else:
            get_excel(sql)
        
        logging.debug(f"{sql.cursor.rowcount} record(s) affected")
        sql.close()
    
