# this is the settings for db module. 

DEBUG = True

VALIDATION_ADDRESS = "https://finance.yahoo.com/quote/"
    
DATABASES = {
    
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ai1",
        "USER": "postgres",
        "PASSWORD": "080802",
        "HOST": "localhost",
        "PORT": "5432",

    }

ASSETDATA_TABLE_NAME = "aiinvest_assetdata"
ASSETLIST_TABLE_NAME = "aiinvest_assetlist"