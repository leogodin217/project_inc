from supplyon_uploader.uploader.sql import generate_query
from supplyon_uploader.uploader.sql import save_query_data
from supplyon_uploader.uploader.sql import generate_bad_data_query
from pathlib import Path
import sqlite3
import pandas as pd

save_dir = Path('.').absolute().parent /'csv'
sql_db = Path('.').absolute() /'test/data/test.db'


config = {
    'mandatory_fields': {
        'field1': 'string',
        'field2': 'integer',
        'field3': 'date'
    },
    'optional_fields': {
        'field4': 'string',
        'field5': 'integer',
        'field6': 'date'
    },
    'customers': ['cust1', 'cust2'],
    'odbc_connection': f'Driver=SQLite3 ODBC Driver;Database={sql_db}',
    'save_dir': save_dir.as_posix(),
    'needed_fields': ['field1', 'field2']
}

def test_generate_query_creates_the_query():
    sql = generate_query(config)
    expected_sql_parts = [
        'select',
        '    field1,',
        '    field2,',
        '    field3,',
        '    field4,',
        '    field5,',
        '    field6',
        'from dbo.supplyon_data_all_customers_needs_update',
        "where customer_id in ('cust1', 'cust2')"
    ]
    expected_sql = '\n'.join(expected_sql_parts)
    print(expected_sql)
    sql.should.equal(expected_sql)

def test_generate_bad_data_query_appends_needed_fields_in_the_query():
    query_parts = [
        'select',
        '    customer_id,',
        '    field1,',
        '    field2',
        'from dbo.supplyon_data_all_customers_needs_update',
        "where customer_id in ('cust1', 'cust2')",
        'and (field1 is null',
        'or field2 is null)'    
    ]
    expected_query = '\n'.join(query_parts)
    query = generate_bad_data_query(config)
    query.should.equal(expected_query)

def test_save_query_data_works():
    # test.db is created in test/data/test.db
    # It contains two rows for id, name
    # [('test1', 1, datetime.datetime(2019, 1, 1, 0, 0), 'test1', 1, datetime.datetime(2019, 1, 1, 0, 0), 'cust1'),
    # ('test2', 2, datetime.datetime(2019, 1, 1, 0, 0), 'test2', 2, datetime.datetime(2019, 1, 1, 0, 0), 'cust2')]"
    sql = 'select * from supplyon'
    result = save_query_data(sql, config)

    data = pd.read_csv(result)
    data.shape.should.equal((2, 7))
    data.columns.should.contain('field1')
    data.columns.should.contain('field2')
    data.columns.should.contain('field3')
    data.columns.should.contain('field4')
    data.columns.should.contain('field5')
    data.columns.should.contain('field6')
    data.columns.should.contain('customer_id')
    data.columns.should_not.contain('id')