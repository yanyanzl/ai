"""
Copyright (C) Steven Jiang. All rights reserved. This code is subject to the terms
 and conditions of the MIT Non-Commercial License, as applicable.
all the settings for the aitrading related modules.

"""
from pynput import keyboard

import yaml
import io

# settingfile to be used.
SETTING_FILE_NAME = 'aisettings.yaml'

ASSET_LIST = []

class Aiconfig():

    # class static variable config is loaded as the unique config data
    config = {}
    
    def __init__(self) -> None:
        self.isconfig = False
    
    @staticmethod
    def _load_config() ->bool:
        """
        """
        success = False
        with open(SETTING_FILE_NAME) as readfile:
            Aiconfig.config = yaml.safe_load(readfile)
        if Aiconfig.config:
            success = True
        return success
    
    @staticmethod
    def get(name:str):
        """ get the value of the specific name in the configuration file
        """
        if name:
            if not Aiconfig.config:
                if not Aiconfig._load_config():
                    raise FileExistsError(f"can't get configuration file loaded. file name: {SETTING_FILE_NAME}")
                
            return Aiconfig.config[name]
        else:
            raise ValueError(f"Name invalid: {name}")

    @staticmethod
    def set(name:str, args):
        """
        set the value of the specific settings
        """
        if not Aiconfig.config:
            if not Aiconfig._load_config():
                raise FileExistsError(f"can't get configuration file loaded. file name: {SETTING_FILE_NAME}")
        
        if name and Aiconfig.config[name] and args:
            Aiconfig.config.update({name: args})

            with open(SETTING_FILE_NAME, 'w') as writefile:
                yaml.dump(Aiconfig.config, writefile)
        else:
            raise ValueError(f"Name invalid: {name} or vlue {args}")

    def add(name:str, **args):
        """
        add a name: values to the settings.
        """
        if not Aiconfig.config:
            if not Aiconfig._load_config():
                raise FileExistsError(f"can't get configuration file loaded. file name: {SETTING_FILE_NAME}")

        if name and args:
            if Aiconfig.config[name]:
                raise ValueError(f"Name already exist: {name}. you can use set() to change the value")
            
            Aiconfig.config[name]= args

            with open(SETTING_FILE_NAME, 'w') as writefile:
                yaml.dump(Aiconfig.config, writefile)
        else:
            raise ValueError(f"Name invalid: {name} or vlue {args}")
        
    def append_to_list(name:str, **args):
        if not Aiconfig.config:
            if not Aiconfig._load_config():
                raise FileExistsError(f"can't get configuration file loaded. file name: {SETTING_FILE_NAME}")
        print("Aiconfig.config[name] is ",Aiconfig.config[name])
        if name and Aiconfig.config[name] and args and isinstance(Aiconfig.config[name],list):
            list(Aiconfig.config[name]).append(args)

            with open(SETTING_FILE_NAME, 'w') as writefile:
                yaml.dump(Aiconfig.config, writefile)
        else:
            raise ValueError(f"Name invalid: {name} or vlue {args}")



# Define data
def initialize_settings_data():
        
    data = {
        'DEBUG' : True,

        'ASSET_LIST': [
            'TSLA', 
            'AAPL', 
            'NVDA', 
            'META', 
            'AMD', 
            'AMZN', 
            'GOOG', 
        ],
        'another dict': {
            'foo': 'bar',
            'key': 'value',
            'the answer': 66
        }, 

        'ACCOUNT_COLUMNS': ['key', 'value', 'currency'],

        'PORTFOLIO_COLUMNS': ['symbol', 'sectype', 'exchange', 'position', 'marketprice', 'marketvalue', 'averagecost', 'unrealizedpnl', 'realizedpnl'], 

        'ACCOUNT_INFO_SHOW_LIST': ['UnrealizedPnL','RealizedPnL', "NetLiquidation","TotalCashValue", "BuyingPower","GrossPositionValue", "AvailableFunds"], 

        'PLACE_BUY_ORDER' : 'key.f4',
        'PLACE_SELL_ORDER' : 'key.f5',

        'CANCEL_LAST_ORDER' : ['key.shift', 'c'],
        'CANCEL_ALL_ORDER' : ['key.shift', 'key.backspace'],

        'PLACE_IOC_BUY' : 'key.f9',

        'PLACE_IOC_SELL' : 'key.f12',

        'PLACE_STOP_BUY' : 'key.f10',
        'PLACE_STOP_SELL' : 'key.f11',

        'PLACE_BRACKET_BUY' : 'key.f7',
        'PLACE_BRACKET_SELL' : 'key.f8',

        'CHANGE_CONTRACT' : 'key.f1',
        'SHOW_CURRENT_CONTRACT' : 'key.f2',

        'REQ_OPEN_ORDER' : ['key.shift', 'o'],
    
        'TICK_BIDASK': ['key.shift', 't'],
        
    
        'CANCEL_TICK_BIDASK': ['key.shift', 'r'],

        'REQUIRE_REALTIME_BAR' : ['key.shift', 'b'],

        'CANCEL_REALTIME_BAR' : ['key.shift', 'v'],
 
        'SHOW_PORT' : ['key.shift', 'p'],
         
        'SHOW_SUMMARY' : ['key.shift', 's'],

        'BUY_LMT_PLUS' : 0.05,
        'SELL_LMT_PLUS' : -0.05,

        'LOGGING_FILE_NAME' : "log/log.txt",
        'SYMBOL_CHANGED' : 'SYMBOL_CHANGED',

        'VALIDATION_ADDRESS' : "https://finance.yahoo.com/quote/"

        }
    
    # ['{keyboard.Key.shift, KeyCode(char="r")},{keyboard.Key.shift, KeyCode(char="R")}]

    # Write YAML file
    with open('aisettings.yaml', 'w', encoding='utf8') as outfile:
        data['ASSET_LIST'].append('COIN')
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    # Read YAML file
    with open("aisettings.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        

    print(data_loaded)




def main():
    
    # initialize the setting file.
    initialize_settings_data()

    # Aiconfig.set("ASSET_LIST", ['TSLA', 'AAPL', 'NVDA', 'META', 'AMD', 'AMZN', 'GOOG', 'COIN','NFLX'])
    # list = Aiconfig.get("ASSET_LIST")
    # print(list)

    # Read YAML file
    # with open("aisettings.yaml", 'r') as stream:
    #     data_loaded = yaml.safe_load(stream)

    # print(data_loaded['PLACE_BUY_ORDER'])
    # al = Aiconfig.get('PLACE_BUY_ORDER')
    # print(type(al).__name__)

if __name__ == "__main__":
    main()

