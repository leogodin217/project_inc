from supplyon_uploader.config.config import get_config
from zeep import Client, Settings
from zeep.plugins import HistoryPlugin
import datetime
import csv
import sys
from copy import deepcopy

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
    
def validate_mandatory_fields(data, config):
    '''
    Ensures all data includes values for the mandatory fields and mandatory
    fields have the correct type.

    Parameters:
        data: A list of dicts, where each dict represents one row of data.
        config: Dict with configuration from config.json

    Returns:
        A list of dicts with the overall status and status of each field
        [{
            'valid': True/False,
            'field1': True/False
        }]
    '''

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

def validate_optional_fields(data, config):
    '''
    Ensures any values provided for optional fields are of the correct type
    Parameters:
        data: A list of dicts, where each dict represents one row of data.
        config: Dict with config from config.json

    Returns:
        A list of dicts with the overall status and status of each field
        [{
            'valid': True/False,
            'field1': True/False
        }]
    '''

    if 'optional_fields' not in config.keys():
        sys.exit('Config file missing optional_fields')
    
    mandatory_fields = config['optional_fields']
    optional_keys = mandatory_fields.keys()
    valid_rows = []
        
    # Loop through the data
    for row in data:
        all_valid = True
        row_validity = {}
        # Loop through each field in the data
        for key in optional_keys:
            if key in row:
                # Check if data type matches configured values in the config file
                field_type = get_data_type(mandatory_fields[key])
                data_value = row[key]
                is_correct_type = isinstance(data_value, field_type) or data_value is None
                row_validity[key] = is_correct_type
                if is_correct_type is False:
                    all_valid = False
            else:
                all_valid = False
                row_validity[key] = False

            row_validity['all_valid'] = all_valid
            valid_rows.append(row_validity)
    # for key in valid_rows[0]:
        # print(f'{key}: {valid_rows[0][key]}')
    return valid_rows

def get_default_data(data_type, config):
    '''
    Returns a configured value from config.json for each supported data type

    Parameters:
        data_type: One of "string", "integer" or "date"
        config: Dict with configuration from config.json
    
    Returns: The default_value for the data type
    '''


    if 'default_values' not in config:
        sys.exit('default_values missing from config.json')
    if data_type not in config['default_values']:
        sys.exit(f'Data type: {data_type} not configured in config.json')
    
    return config['default_values'][data_type]

def set_default_values(data, config):
    '''
    Sets default values for any required fields that are missing values.

    Parameters:
        data: A list of dicts where each dict represents one row of data
        config: Dict with configuration from config.json

    Returns: A list of dicts with required missing fields filled in.
    '''
    # Ensure we do not overwrite original data
    set_data = deepcopy(data)
    if 'mandatory_fields' not in config:
        sys.exit('mandatory_fields is missing from config.json')
    
    mandatory_fields = config['mandatory_fields']
    for row in set_data:
        for field, data_type in mandatory_fields.items():
            if row[field] is None:
                row[field] = get_default_data(data_type, config) 

    return set_data

def fill_missing_values(data):
    '''
    replaces empty strings with None

    Parameters:
        data: A list of dicts where each dict represents one row of data

    Returns: A new list of dicts with empty strings replaced with None
    '''
    # Ensure we do not modify the original data
    none_data = deepcopy(data)

    for row in none_data:
        for field, value in row.items():
            if value == '':
                row[field] = None
    return none_data