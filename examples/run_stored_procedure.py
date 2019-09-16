from supplyon_uploader.config.config import get_config
from supplyon_uploader.uploader.sql import run_stored_procedure
from supplyon_uploader.uploader.sql import upload_workcenter_codes
from pathlib import Path

config_path = Path('C:\\supplyon\\config.json')

config = get_config(config_path)

# UPload the latest workcenter codes
upload_workcenter_codes(config)

# Run the stored procedure that pulls the data
run_stored_procedure(config)
