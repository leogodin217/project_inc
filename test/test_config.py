from supplyon_uploader.config.config import get_config
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