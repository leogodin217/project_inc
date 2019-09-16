''' Prepares and uploads data to the SupplyOn portal'''
from supplyon_uploader.config.config import get_config
from supplyon_uploader.uploader.sql import generate_query
from supplyon_uploader.uploader.sql import save_query_data
from supplyon_uploader.uploader.data import get_data
from supplyon_uploader.uploader.data import set_default_values
from supplyon_uploader.uploader.data import fill_missing_values
from supplyon_uploader.uploader.data import set_data_types
from supplyon_uploader.uploader.upload import get_client
from supplyon_uploader.uploader.upload import prepare_data
from supplyon_uploader.uploader.upload import upload_data
from pathlib import Path

#
config_path = Path('C:\\supplyon\\config.json')
config = get_config(config_path)

# Get the data and save to a CSV file
query = generate_query(config)
query_result = save_query_data(query, config)

# Read in the data and clean it
data = get_data(query_result)
default_data = set_default_values(data, config)
none_data = fill_missing_values(default_data)
typed_data = set_data_types(none_data, config)
print(f'Prepared {len(typed_data)} records')

# Prepare the data and upload it. 
client = get_client(config)
prepared_data = prepare_data(typed_data, config)
result = upload_data(prepared_data, client)
print(result)
