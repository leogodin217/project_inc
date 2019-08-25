from supplyon_uploader.config.config import get_config
from zeep import Client, Settings
from zeep.plugins import HistoryPlugin
import datetime
import csv
import sys

def get_data(file_path):
    '''
    Creates a list of dicts from a CSV file, with one dict per row.

    Parameters:
        file_path - A pathlib.Path object representing the full path to the
                    file. 

    Returns:
        A list of dicts, with one dict for each row in the file
    '''

    records = []
    with open(file_path, 'r') as f:
        data_reader = csv.reader(f)
        data = [row for row in data_reader]
        columns = data[0]
        for row in data[1:len(data)]:
            record = {}
            for index, key in enumerate(columns):
                record[key] = row[index]
            records.append(record)
    return(records)

def get_data_type(description):
    '''
    Returns a valid python type from a string input. This is used to 
    validate data, where the data description is in the config file. 

    returns:
        A python type. 
    '''
    data_type = None
    data_types = {
        'string': str,
        'integer': int,
        'date': datetime.datetime
    } 

    if description not in data_types:
        data_type = False
    else: 
        data_type = data_types[description]
    return data_type
    
def validate_mandatory_fields(data):
    '''
    Ensures all data includes values for the mandatory fields and mandatory
    fields have the correct type.

    Parameters:
        data: A list of dicts, where each dict represents one row of data.

    Returns:
        A list of dicts with the overall status and status of each field
        [{
            'valid': True/False,
            'field1': True/False
        }]
    '''

    config = get_config()
    if 'mandatory_fields' not in config.keys():
        sys.exit('Config file missing mandatory_fields')
    
    mandatory_fields = config['mandatory_fields']
    mandatory_keys = mandatory_fields.keys()
    valid_rows = []
        
    # Loop through the data
    for row in data:
        all_valid = True
        row_validity = {}
        # Loop through each field in the data
        for key in mandatory_keys:
            if key in row:
                # Check if data type matches configured values in the config file
                field_type = get_data_type(mandatory_fields[key])
                data_value = row[key]
                is_correct_type = isinstance(data_value, field_type)
                row_validity[key] = is_correct_type
                if is_correct_type is False:
                    all_valid = False
            else:
                all_valid = False
                row_validity[key] = False

            row_validity['all_valid'] = all_valid
            valid_rows.append(row_validity)
    return valid_rows



        