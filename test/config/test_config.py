from supplyon_uploader.config.config import get_config
from datetime import datetime
import sure

def test_get_config_returns_a_dict():
    config = get_config()
    config.should.be.a(dict)

def test_get_config_contains_headers():
    config = get_config()
    config.should.have.key('supplyon_headers')

def test_headers_are_lists_of_dicts():
    config = get_config()
    config['supplyon_headers'].should.be.a(list)
    for header in config['supplyon_headers']:
        header.should.be.a(dict)

def test_supplyon_url_exists():
    config = get_config()
    config.should.have.key('supplyon_url')
    config['supplyon_url'].should.be.a(str)

def test_mandatory_fields_is_dict():
        config = get_config()
        config.should.have.key('mandatory_fields')
        config['mandatory_fields'].should.be.a(dict)

def test_mandatory_field_items_are_numeric_date_or_text():
        config = get_config()
        mandatory_fields = config['mandatory_fields']
        for key in mandatory_fields.keys():
                mandatory_fields[key].should.be.within(['string', 'integer', 'date'])

def test_optional_fields_is_dict():
        config = get_config()
        config.should.have.key('optional_fields')
        config['optional_fields'].should.be.a(dict)

def test_optional_field_items_are_numeric_or_text():
        config = get_config()
        optional_fields = config['optional_fields']
        for key in optional_fields.keys():
                optional_fields[key].should.be.within(['string', 'integer', 'date'])

def test_config_has_default_string():
        config = get_config()
        config.should.have.key('default_values')
        config['default_values'].should.have.key('string')

def test_config_has_default_integer():
        config = get_config()
        config.should.have.key('default_values')
        config['default_values'].should.have.key('integer')

def test_config_has_default_date():
        config = get_config()
        config.should.have.key('default_values')
        config['default_values'].should.have.key('date')
