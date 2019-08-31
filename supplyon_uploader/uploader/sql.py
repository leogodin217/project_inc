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

    query = 'select\n' 
    select_parts = []
    # Append the fields prepended with four spaces for formatting
    for key in config['mandatory_fields'].keys():
        select_parts.append('    ' + key)
    for key in config['optional_fields'].keys():
        select_parts.append('    ' + key)
    query += ',\n'.join(select_parts)
    # Add the table
    query += f'\nfrom ##supply_on_data_all_customers'
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
    query = generate_query(config) 
    for field in config['needed_fields']:
        query += f'\nand {field} is not null'
    print(query)
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
    conn = pyodbc.connect(odbc_connection)
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
    conn = pyodbc.connect(odbc_connection)
    success = True
    drop_query = f'drop table if exists ##supply_on_data_bad_data'
    full_query = f'select * into  ##supply_on_data_bad_data from ({query}) as data'
    try:
        conn.execute(drop_query)
        conn.execute(full_query)
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
    conn = pyodbc.connect(odbc_connection)
    success = True
    try:
        conn.execute('{call dbo.get_supply_on_data_all_customers (?)}', min_date)
    except Exception as e:
        sys.exit(e.args)