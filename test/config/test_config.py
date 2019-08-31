from supplyon_uploader.config.config import get_config
from datetime import datetime
from pathlib import Path
import sure

config_path = Path('.').absolute().parent /'config.json'

def test_get_config_returns_a_dict():
    config = get_config(config_path)
    config.should.be.a(dict)

def test_get_config_contains_headers():
    config = get_config(config_path)
    config.should.have.key('supplyon_headers')

def test_headers_are_lists_of_dicts():
    config = get_config(config_path)
    config['supplyon_headers'].should.be.a(dict)

def test_mandatory_fields_is_dict():
        config = get_config(config_path)
        config.should.have.key('mandatory_fields')
        config['mandatory_fields'].should.be.a(dict)

def test_mandatory_field_items_are_numeric_date_or_text():
        config = get_config(config_path)
        mandatory_fields = config['mandatory_fields']
        for key in mandatory_fields.keys():
                mandatory_fields[key].should.be.within(['string', 'integer', 'date'])

def test_optional_fields_is_dict():
        config = get_config(config_path)
        config.should.have.key('optional_fields')
        config['optional_fields'].should.be.a(dict)

def test_optional_field_items_are_numeric_or_text():
        config = get_config(config_path)
        optional_fields = config['optional_fields']
        for key in optional_fields.keys():
                optional_fields[key].should.be.within(['string', 'integer', 'date'])

def test_config_has_default_string():
        config = get_config(config_path)
        config.should.have.key('default_values')
        config['default_values'].should.have.key('string')

def test_config_has_default_integer():
        config = get_config(config_path)
        config.should.have.key('default_values')
        config['default_values'].should.have.key('integer')

def test_config_has_default_date():
        config = get_config(config_path)
        config.should.have.key('default_values')
        config['default_values'].should.have.key('date')

def test_config_has_wsdl():
        config = get_config(config_path)
        config.should.have.key('wsdl')

def test_config_has_customers():
        config = get_config(config_path)
        config.should.have.key('customers')
        config['customers'].should.be.a(list)
        for item in config['customers']:
                item.should.be.a(str)

def test_config_has_odbc_connection_info():
        config = get_config(config_path)
        config.should.have.key('odbc_connection')
        config['odbc_connection'].should.be.a(str)

def test_config_has_min_date():
        config = get_config(config_path)
        config.should.have.key('min_date')
        config['min_date'].should.be.a(str)