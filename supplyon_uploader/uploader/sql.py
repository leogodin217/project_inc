''' Creates and runs queries '''
import sys
import pandas as pd
import pyodbc
from pathlib import Path
import datetime
from copy import deepcopy

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

    query = 'select\n' 
    select_parts = []
    # Append the fields prepended with four spaces for formatting
    for key in config['mandatory_fields'].keys():
        select_parts.append('    ' + key)
    for key in config['optional_fields'].keys():
        select_parts.append('    ' + key)
    query += ',\n'.join(select_parts)
    # Add the table
    query += f'\nfrom dbo.supplyon_data_all_customers_needs_update'
    # Add the where clause
    query += "\nwhere customer_id in ('"
    customers = "', '".join(config['customers'])
    query += customers + "')"

    return query

def generate_bad_data_query(config):
    '''
    Bad data does not have one of "needed_fields" in the config. This data 
    cannot be updated

    Params:
        config: Dict containing configuraiton from config.json
    
    Returns: String representing the query
    '''
    if 'needed_fields' not in config:
        sys.exit('needed_fields not in configuration')
    needed_fields = deepcopy(config['needed_fields'])
    query = 'insert into dbo.supplyon_bad_data\nselect\n' 
    select_parts = ['    customer_id']
    # Append the fields prepended with four spaces for formatting
    for key in needed_fields:
        select_parts.append('    ' + key)
    query += ',\n'.join(select_parts)
    # Add the table
    query += f'\nfrom dbo.supplyon_data_all_customers_needs_update'
    # Add the where clause
    query += "\nwhere customer_id in ('"
    customers = "', '".join(config['customers'])
    query += customers + "')"
    # Append the where clause
    # We want the first field to set up this clause
    needed_fields.reverse()
    first_needed_field = needed_fields.pop()
    query += f'\nand ({first_needed_field} is null'
    for key in needed_fields:
        query += f'\nor {key} is null'
    query += ')'
    return query

def save_query_data(query, config):
    '''
    Runs the query and saves the data to a CSV file

    Parameters:
        query: String witht the query to use
        config: Dict with configuration information from config.json
    
    Returns: Path object of the saved CSV file 
    '''

    if 'odbc_connection' not in config:
        sys.exit('odbc_connection missing from config.json')
    if 'save_dir' not in config:
        sys.exit('save_dir missing from config.json')

    odbc_connection = config['odbc_connection']
    conn = pyodbc.connect(odbc_connection, autocommit=True)
    save_path = Path(config['save_dir']).absolute()
    save_path.mkdir(exist_ok=True)
    file_name = 'supplyon-' + str(datetime.datetime.now().timestamp()) + '.csv'
    save_file = save_path /file_name    

    try:
        data = pd.read_sql(con=conn, sql=query)
        data.to_csv(save_file, index=False)
    except Exception as e:
        sys.exit(e.args)
    return save_file 

def save_bad_data(query, config):
    '''
    Saves bad data to a temp table for later email. Bad data are records that
    have null values for any of the needed_fields in the config

    Parameters:
        query: String representing the query to use for bad data
        config: Dict with configuraiton information from config.json
        returns: Bool indicating success or failure
    '''

    if 'odbc_connection' not in config:
        sys.exit('odbc_connection missing from config.json')
    odbc_connection = config['odbc_connection']
    conn = pyodbc.connect(odbc_connection, autocommit=True)
    success = True
    drop_query = f'truncate table dbo.supplyon_bad_data'
    full_query = f'insert into dbo.supplyon_bad_data  {query} as data'
    try:
        result = conn.execute(drop_query)
        result.close()
        result = conn.execute(full_query)
        result.close()
        conn.close()
    except:
        sys.exit(e.args)
    return success 

def run_stored_procedure(config):
    '''
    Runs the main stored procedure to gather data

    Parameters:
        config: Dict containing configuration inforamtion from config.json
    
    Returns: Bool indicating success or failure
    '''
    if 'odbc_connection' not in config:
        sys.exit('odbc_connection missing from config.json')
    if 'min_date' not in config:
        sys.exit('min_date missing from configuration')
    min_date = None
    try:
        min_date = datetime.datetime.fromisoformat(config['min_date'])    
    except Exception as e:
        sys.exit('Could not convert min_date to datetime')

    odbc_connection = config['odbc_connection']
    conn = pyodbc.connect(odbc_connection, autocommit=True)
    success = True
    try:
        result = conn.execute('{call dbo.get_supply_on_data_all_customers (?)}', min_date)
        result.close()
        conn.close()
    except Exception as e:
        sys.exit(e.args)