''' Creates and runs queries '''
import sys
import pandas as pd
import pyodbc
from pathlib import Path
import datetime

def generate_query(config):
    '''
    Generates a query from the config based on mandatory_fields and 
    optional_fields, and customers

    Params:
        config: Dict containing configuration from config.json

    Returns: A string with the SQL command to select all fields, using
             a where clause with the customers 
    '''
    if 'mandatory_fields' not in config:
        sys.exit('mandatory_fields not in configuration')
    if 'optional_fields' not in config:
        sys.exit('optional_fields not in configuration')
    if 'customers' not in config:
        sys.exit('customers not in configuration')
    if 'data_table' not in config:
        sys.exit('data_table not in configuration')

    query = 'select\n' 
    select_parts = []
    # Append the fields prepended with four spaces for formatting
    for key in config['mandatory_fields'].keys():
        select_parts.append('    ' + key)
    for key in config['optional_fields'].keys():
        select_parts.append('    ' + key)
    query += ',\n'.join(select_parts)
    # Add the table
    query += f'\nfrom {config["data_table"]}'
    # Add the where clause
    query += "\nwhere customer_id in ('"
    customers = "', '".join(config['customers'])
    query += customers + "')"
    return query

def save_query_data(query, config):
    '''
    Runs the query and saves the data to a CSV file

    Parameters:
        query: String witht the query to use
        config: Dict with configuration information from config.json
    
    Returns: Bool indicating success or failure
    '''

    if 'odbc_connection' not in config:
        sys.exit('odbc_connection missing from config.json')
    if 'save_dir' not in config:
        sys.exit('save_dir missing from config.json')

    odbc_connection = config['odbc_connection']
    conn = pyodbc.connect(odbc_connection)
    save_path = Path(config['save_dir']).absolute()
    file_name = 'supplyon-' + str(datetime.datetime.now()) + '.csv'
    save_file = save_path /file_name    

    try:
        data = pd.read_sql(con=conn)
        data.to_csv(save_file)
    except Exception as e:
        sys.exit(e.args)
    return True

    