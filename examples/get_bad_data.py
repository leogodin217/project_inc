'''Pulls records for upload that have null values for needed_fields in config'''
from supplyon_uploader.config.config import get_config
from supplyon_uploader.uploader.sql import generate_bad_data_query
from supplyon_uploader.uploader.sql import save_bad_data
from pathlib import Path

config_path = Path('C:\\supplyon\config.json')

config = get_config(config_path)
query = generate_bad_data_query(config)
save_bad_data(query, config)
