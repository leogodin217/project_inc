''' Manages configuration environment  '''
from pathlib import Path
import json

def get_config():
    '''
    Settings are configured in a config file that is one directory up from the
    base code directory. We need to understand the location of the CSV files
    and connection information for the SupplyOn portal. Settings are held in
    ../supply_on_config.json

    Returns a dict with {
        'supplyon_url': 'URL to the SupplyOn web service',
        'supplyon_headers: {
            'header1': 'header',
            'header2': 'header 2',
            ...
        }
    }

    Current expected headers include the ones below. But new headers can be
    added to the config file. 
    'Ocp-Apim-Subscription-Key': '',
    'Content-Type': 'text/xml',
    'SOAPAction': 'http://gateway.api.qas.supplyon.com/ProductionToSupply'
    '''

    config_file = Path('..').absolute() /'config.json'

    config = None
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    return config
