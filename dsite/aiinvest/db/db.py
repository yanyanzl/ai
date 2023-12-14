
# this is the module for all database operation realted functions and features.

import psycopg2
from db_settings import DATABASES as dbs
from db_settings import DEBUG

from finlib import format_excetpion_message
from finlib import Asset
import requests
import pprint

DEFAULT_DATABASE = dbs['NAME']
DEFAULT_USER = dbs['USER']
DEFAULT_HOST= dbs['HOST']
DEFAULT_PASSWORD = dbs['PASSWORD']
DEFAULT_PORT = dbs['PORT']

# get a connection to database. inner function. 
# Open a cursor to perform database operations
def _get_conn(db=DEFAULT_DATABASE, dbhost=DEFAULT_HOST, dbport=DEFAULT_PORT, dbuser=DEFAULT_USER,dbpass=DEFAULT_PASSWORD):

        try:
            # build the connection to the database by psycopg2
            conn = psycopg2.connect(database=db, 
                    user=dbuser, host=dbhost, password=dbpass,port=dbport)
            return conn
        except Exception as ex:
            format_excetpion_message(ex)

# development test. should be deleted when deploy.
def test_tmp():
        
        conn = _get_conn()
        cur = conn.cursor()

        cur.execute("SELECT * from aiinvest_assetlist")

        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur.execute("SELECT * from aiinvest_assetdata")
        rows = cur.fetchall()

        for row in rows:
            print(row)


        # this will get all the table's information .
        cur.execute("""SELECT *
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE' and TABLE_SCHEMA = 'public'""")
        rows = cur.fetchall()

        for row in rows:
            print(row)


        # this will get all the table's columns' information .
        cur.execute("""SELECT * FROM information_schema.columns
        WHERE table_name = 'aiinvest_assetdata'""")
        rows = cur.fetchall()

        for row in rows:
            print(row)

        # Make the changes to the database persistent
        conn.commit()

        
        cur.close()

        conn.close()


# get the asset id by asset name. if can't find the id. raise valueerror.
def get_asset_id(asset_name=""):
        
        try:
            # construct SQL 
            query = "SELECT id from aiinvest_assetlist where asset_name=\'" + asset_name +"\'"
            conn = _get_conn()
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            # Make the changes to the database persistent
            conn.commit()
            cur.close()
            conn.close()

            if DEBUG:
                print(rows[0][0])
            
            if len(rows) != 1:
                raise ValueError(f"there is {len(rows)} asset in the db for asset_name: {asset_name}")
            return rows[0][0]
        except Exception as ex:
            format_excetpion_message(ex)


# get_asset_id("TSLA")

# get data online and save to database. 
# years is number of yesrs to build the data. default is the current year till now
def _build_asset_data(asset_name="", years=0):
        asset = Asset(asset_name)
        try:

            if not asset.is_valid():
                raise ValueError (f"Asset data is not found for Asset name : {asset_name}")
            
            his_price = asset.fetch_his_price(period=years)
            
            if DEBUG:
                print(len(his_price))

        except Exception as ex:
            format_excetpion_message(ex)


# add asset_data to aiinvest_assetdata table in database
def _add_data_to_db():
    ...

_build_asset_data("TSLA", 3)
