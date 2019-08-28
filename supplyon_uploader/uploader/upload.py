''' Prepares and uploads data to the SupplyOn Portal '''
from supplyon_uploader.config.config import get_config
from pathlib import Path
from zeep import Client, Settings
import sys


def get_wsdl(config):
    '''
    Gets the file path for the WSDL

    Parameters:
        config: Dict with configuration values from config.json

    Returns: A string with the posix path for the WSDL
    '''
    if "wsdl" not in config:
        sys.exit('wsdl is not defined in config.json') 
    wsdl_dir = Path('.').absolute().parent
    wsdl = wsdl_dir /config['wsdl']
    print(Path('.').absolute())
    print(wsdl.as_posix())
    return wsdl.as_posix()

def get_client(config):
    '''
    Creates a zeep Client with configured information

    Parameters:
        config: Dict with configuration information from config.json

    Returns: A configured zeep.Client
    '''
    if 'supplyon_headers' not in config:
        sys.exit('supplyon_headers not configured in config.json')
    headers = config['supplyon_headers']
    wsdl = get_wsdl()
    settings = Settings(extra_http_headers=headers)
    client = Client(wsdl=wsdl, settings=settings)
    return client

def prepare_data(data, config):
    '''
    Prepares data for SupplyOn upload using the SupplyOn WSDL data types

    Parameters:
        data: A list of dicts wher each dict represents one row of data
        config: Dict with configuration information from config.json

    Returns: ArrayOfProductionData with one ProductionData per item in data.
             These types are per the SupplyOn WSDL
    '''
    if 'supplyon_headers' not in config:
        sys.exit('headers not configured in config.json')

    return data    
