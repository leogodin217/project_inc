from supplyon_uploader.uploader.sql import generate_query
from supplyon_uploader.uploader.sql import save_query_data
from pathlib import Path

save_dir = Path('.').absolute().parent /'csv'


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
    'data_table': 'mytable',
    'odbc_connection': "test",
    'save_dir': save_dir
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
        'from mytable',
        "where customer_id in ('cust1', 'cust2')"
    ]
    expected_sql = '\n'.join(expected_sql_parts)
    print(expected_sql)
    sql.should.equal(expected_sql)

def test_save_query_data_works():
    sql = generate_query(config)
    result = save_query_data(sql, config)
