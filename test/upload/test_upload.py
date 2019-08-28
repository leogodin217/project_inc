from supplyon_uploader.uploader.upload import get_wsdl
from supplyon_uploader.uploader.upload import get_client
from supplyon_uploader.config.config import get_config
from supplyon_uploader.uploader.upload import prepare_data
from pathlib import Path
import string
import random
import datetime
import pytest
import sure


config_path = Path('.').absolute().parent /'config.json'
config = get_config(config_path)

def test_wsdl_path_returns_wsdl_one_directory_up():
    expected_path = Path('.').absolute().parent
    expected_wsdl_name = config['wsdl']
    expected_full_path = expected_path /expected_wsdl_name
    wsdl = get_wsdl(config)
    wsdl.should.equal(expected_full_path.as_posix())  

def test_get_client():
    client = get_client(config)
    response = client.service.ProductionToSupply()
    response.should.equal('ProductionDataList is empty.')

    
@pytest.fixture()
def full_record():
    record = {}
    for field, data_type in config['mandatory_fields'].items():
        if data_type == 'string':
            # Generate a random string
            letters = string.ascii_letters
            record[field] = ''.join([random.choice(letters) for i in range(len(letters[0:10]))])
        elif data_type == 'integer':
            record[field] = 0
        elif data_type == 'date':
            record[field] = datetime.datetime.now()
    for field, data_type in config['optional_fields'].items():
        if data_type == 'string':
            # Generate a random string
            letters = string.ascii_letters
            record[field] = ''.join([random.choice(letters) for i in range(len(letters[0:10]))])
        elif data_type == 'integer':
            record[field] = 0
        elif data_type == 'date':
            record[field] = datetime.datetime.now()
    return record

def test_prepare_data_returns_array_of_production_data(full_record):
    data = [full_record, full_record]
    prepared_data = prepare_data(data, config)
    str(type(prepared_data)).should.equal("<class 'zeep.objects.ArrayOfProductionData'>")

def test_prepare_data_array_of_production_data_is_a_list_of_production_data(full_record):
    data = [full_record, full_record]
    prepared_data = prepare_data(data, config)
    data_list = prepared_data.ProductionData
    data_list.should.be.a(list)
    for key, value in data[0].items():
        data_list[0][key].should.equal(value)
        data_list[1][key].should.equal(value)



