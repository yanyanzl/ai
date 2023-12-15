
# this is the module for all database operation realted functions and features.

import psycopg2
from db_settings import DATABASES as dbs
from db_settings import DEBUG, ASSETDATA_TABLE_NAME,ASSETLIST_TABLE_NAME
import pandas as pd

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



# get the asset id by asset name. 
# if can't find the id. check it online, 
# if the asset is an valid ticker, insert it into the table
# otherwise raise valueerror.
# 
def get_asset_id(asset_name=""):
        asset_id = -1
        try:
            # construct SQL 
            query = "SELECT id from aiinvest_assetlist where asset_name=\'" + asset_name +"\'"
            conn = _get_conn()
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            conn.commit()
            cur.close()

            if DEBUG:
                print(rows)
            
            if len(rows) == 1:
                asset_id = rows[0][0]
            # if the asset doesn't exist in the database. insert it into it
            elif len(rows) == 0 and Asset(asset_name).is_valid():
                 asset_id = _add_asset_to_list(asset_name, ASSETLIST_TABLE_NAME)
            else:
                  conn.close()
                  raise ValueError(f"there is {len(rows)} asset in the db for asset_name: {asset_name}. or the asset_name may be an invalid ticker")
            
            conn.close()
            return asset_id
        except Exception as ex:
            conn.close()
            format_excetpion_message(ex)

# add the asset_name to the asset list table. return the id for the asset.
def _add_asset_to_list(asset_name="", table_name=""):
        try:
            # check the args are correct type
            if  isinstance(asset_name, str):
                # check the list is not empty
                asset_name = pd.DataFrame({'asset_name':[asset_name]})
                
                # provide information for debug
                if DEBUG:
                    print(f" asset_name is {asset_name} and table name is {table_name} in _add_asset_to_list",  )
                
                _add_data_to_db(asset_name, table_name)
 
            # type of the args data inputs are not correct, 
            else:
                raise TypeError(
                    f"string expected for asset name, got'{type(asset_name).__name__}'"
                )
        except Exception as ex:
            format_excetpion_message(ex)



# get_asset_id("TSLA")

# get data online and save to database. 
# years is number of yesrs to build the data. default is the current year till now
def _build_asset_data(asset_name="", years=0, table_name=ASSETDATA_TABLE_NAME):
        asset = Asset(asset_name)
        try:

            if not asset.is_valid():
                raise ValueError (f"Asset data is not found for Asset name : {asset_name}")
            
            asset_id = get_asset_id(asset_name)

            his_price = asset.fetch_his_price(period=years).reset_index()

            his_price['name'] = asset_name
            his_price['asset_id'] = asset_id
            his_price.pop('Adj Close')
            # his_price = his_price.rename(columns={'Date': 'asset_data_date', 
            #                           'Open': 'asset_open_price', 
            #                           'High': 'asset_high_price',
            #                           'Low': 'asset_low_price',
            #                           'Close': 'asset_close_price',
            #                           'Volume': 'asset_volume'
            #                           })

            his_price.columns = map(str.lower, his_price.columns)
            print(his_price)
            

            # _add_data_to_db()
                 # add the price to the table.
            # print("his_price.index ------ ",his_price.index)
            # print("his_price.columns ------ ",his_price.columns)

            for price in his_price:
                # print("his_price.loc[0] ------ ",his_price.loc[0])
                print("price ------ ",price)
                # 
            # _add_data_to_db(his_price,table_name)


            if DEBUG:
                print(len(his_price))

        except Exception as ex:
            format_excetpion_message(ex)



# add data to the specified table in the current connected database
# the column names in data_list should be the same as the table's column names 
def _add_data_to_db(data_list=pd.DataFrame(), table_name=""):
    
    try:
        # check the args are correct type
        if  isinstance(data_list, pd.DataFrame) :
            # check the list is not empty
            if len(data_list) != 0:
                conn = _get_conn()

                cur = conn.cursor()

                query = "insert into "+ table_name + " ("
                
                
                for _ in data_list.columns:
                     query = query + f"{_} ,"
                #  (asset_name,asset_data_date,asset_close_price,asset_open_price,asset_high_price,asset_low_price,asset_volume,asset_id) values ('"+asset_name+"','"
                query = query.rstrip(query[-1])+") values ("

                

                for i in data_list.index:
                    # each row of the Data_list is a row to be inserted.
                    queryi = query
                    for _ in data_list.columns:
                        queryi = queryi + f"'{data_list.iloc[i][_]}'," 
                    
                    queryi = queryi.rstrip(queryi[-1])+")"
                    print(queryi)
                    ############################# to be continue : avoid insert repeatidly
                
                print(len(data_list.columns))
                #  + "'," + f"{his_price.iloc[i]['Close']}" + "," + f"{his_price.iloc[i]['Open']}" + "," + f"{his_price.iloc[i]['High']}" + "," + f"{his_price.iloc[i]['Low']}" + "," + f"{his_price.iloc[i]['Volume']}" + "," + f"{asset_id}" + ")"

                # provide information for debug
                if DEBUG:
                    print("data_list is", data_list)


                conn.commit()
                conn.close
            # input list is empty
            else:
                raise Exception("The input data list is empty for _add_data_to_db or tablename")

        # type of the args data inputs are not correct, 
        else:
            raise TypeError(
                "DataFrame expected for data_list, "+
                f"got'{type(data_list).__name__}'"
            )

    except Exception as ex:
        format_excetpion_message(ex)

# check if the table exist in the current database. 
def is_table_valid(conn, table_name=""):
        exist = False
        try:
             
            query1 = "SELECT EXISTS (SELECT FROM information_schema.tables" + " WHERE table_name = '" + table_name + "');"

            cur = conn.cursor()

            cur.execute("SELECT * from aiinvest_assetlist")

            exist = cur.fetchone()[0]
            print(exist)
            cur.close()
        except Exception as ex:
             format_excetpion_message(ex)
        return exist

# _build_asset_data("TSLA", 0)


# ##################
# development test. should be deleted when deploy.
def test_tmp():
        asset_name="AAPL"
        asset_name = pd.DataFrame({'asset_name':[asset_name], 'asset_id':[1]})
        print(asset_name)
        _add_data_to_db(asset_name, ASSETLIST_TABLE_NAME)

''' 
conn = _get_conn()
cur = conn.cursor()

cur.execute("SELECT * from aiinvest_assetlist")

rows = cur.fetchall()

for row in rows:
    print(row)
# cur.execute("SELECT * from aiinvest_assetdata")
# rows = cur.fetchall()

# for row in rows:
#     print(row)


# this will get all the table's information .
# cur.execute("""SELECT *
# FROM INFORMATION_SCHEMA.TABLES
# WHERE TABLE_TYPE = 'BASE TABLE' and TABLE_SCHEMA = 'public'""")
# rows = cur.fetchall()

# for row in rows:
#     print(row)


# this will get all the table's columns' information .
# cur.execute("""SELECT * FROM information_schema.columns
# WHERE table_name = 'aiinvest_assetdata'""")

table_name = "aiinvest_assetdata"
query = "SELECT column_name FROM information_schema.columns WHERE table_name ='"+table_name+"'"

query1 = "SELECT EXISTS (SELECT FROM information_schema.tables" + " WHERE table_name = '" + table_name + "');"

# this will get all the column_name from the table .
cur.execute(query1)
rows = cur.fetchall()

for row in rows:
    print(row)

print(rows)
# Make the changes to the database persistent
conn.commit()


cur.close()

conn.close()
'''

test_tmp()