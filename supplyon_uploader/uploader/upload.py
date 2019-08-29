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
    wsdl = Path(config['wsdl']) 
    if not wsdl.exists():
        sys.exit(f'Wsdl does not exist {wsdl.absolute()}')
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
    print(headers)
    wsdl = get_wsdl(config)
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
    
    client = get_client(config)

    # These are the data types from the WSDL
    ArrayOfProductionData = client.get_type('ns0:ArrayOfProductionData')
    ProductionData = client.get_type('ns0:ProductionData')
    production_data = ArrayOfProductionData(
        [ProductionData(**field) for field in data]
    )
    return production_data    

def upload_data(data, client):
    '''
    Uploads data to the SupplyOn api

    Parameters:
        data: ArrayOfProductionData with one ProductionData for each row of
              data. This should be prepared with prepare_data

    returns: Status messge
    '''
    response = ''
    try:
        response = client.service.ProductionToSupply(ProductionDataList=data)
    except Exception as e:
        sys.exit(e.args)
    return response

