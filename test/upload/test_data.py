from supplyon_uploader.uploader.data import get_data
from supplyon_uploader.uploader.data import get_data_type
from supplyon_uploader.uploader.data import validate_mandatory_fields
from supplyon_uploader.uploader.data import validate_optional_fields
from supplyon_uploader.uploader.data import get_default_data
from supplyon_uploader.uploader.data import set_default_values
from supplyon_uploader.uploader.data import fill_missing_values
from supplyon_uploader.uploader.data import set_data_types
from supplyon_uploader.config.config import get_config
import datetime
from pathlib import Path 
from copy import deepcopy
import random 
import string
import pytest

# Config is used often
config_path = Path('.').absolute().parent /'config.json'
config = get_config(config_path)

test_data_path = Path('.').absolute() /'test/data/test_data.csv'

def test_get_data_returns_a_list_of_dicts():
    data = get_data(test_data_path)
    data.should.be.a(list)
    for row in data:
        row.should.be.a(dict)

def test_get_data_type_handles_string():
    get_data_type('string')().should.be.a(str)


def test_get_data_type_handles_int():
    get_data_type('integer')().should.be.a(int)

def test_get_data_type_handles_date():
    get_data_type('date').now().should.be.a(datetime.datetime)

def test_get_data_invalid_descriptions_return_false():
    get_data_type('str').should.be.false
    get_data_type(str).should.be.false
    get_data_type(datetime).should.be.false

# Test mandatory fields and do a little setup.

mandatory_fields = [key for key in config['mandatory_fields']]
@pytest.fixture()
def valid_record():
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
    return record
    
def test_validate_mandatory_fields_passes_valid_data(valid_record):
    data = [deepcopy(valid_record), deepcopy(valid_record)]
    valid_data = validate_mandatory_fields(data, config)
    valid_data.should.be.a(list)
    valid_data[0].should.be.a(dict)
    valid_data[0]['all_valid'].should.be.true
    for key in mandatory_fields:
        valid_data[0][key].should.be.true 
    
    valid_data[1].should.be.a(dict)
    valid_data[1]['all_valid'].should.be.true
    for key in mandatory_fields:
        valid_data[1][key].should.be.true

def test_validate_mandatory_fields_fails_missing_field(valid_record):
    missing_data =  [deepcopy(valid_record), deepcopy(valid_record)]
    missing_data[0].pop('Part_Material_Number_Buyer')
    valid_data = validate_mandatory_fields(missing_data, config)
    valid_data[0]['all_valid'].should.be.false
    valid_data[0]['Part_Material_Number_Buyer'].should.be.false

def test_validate_mandatory_fields_fails_with_missing_data(valid_record):
    missing_data = [deepcopy(valid_record), deepcopy(valid_record)]
    missing_data[0]['Part_Material_Number_Buyer'] = None
    valid_data = validate_mandatory_fields(missing_data, config)
    valid_data[0]['all_valid'].should.be.false
    valid_data[0]['Part_Material_Number_Buyer'].should.be.false

def test_validate_mandatory_fields_fails_wrong_type(valid_record):
    missing_data = [deepcopy(valid_record), deepcopy(valid_record)]
    # This should be a string
    missing_data[0]['Part_Material_Number_Buyer'] = 0 
    # This should be a datetime.datetime
    missing_data[0]['Planned_Production_Start_Date'] = 0 
    # This should be an integer
    missing_data[0]['Actual_Start_Production_Qty'] = '0' 

    valid_data = validate_mandatory_fields(missing_data, config)
    valid_data[0]['all_valid'].should.be.false
    valid_data[0]['Part_Material_Number_Buyer'].should.be.false
    valid_data[0]['Planned_Production_Start_Date'].should.be.false
    valid_data[0]['Actual_Start_Production_Qty'].should.be.false

# Test optional fields
optional_fields = [field for field in config['optional_fields']]
@pytest.fixture()
def optional_record():
    record = {}
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


def test_validate_optional_fields_passes_valid_data(optional_record):
    valid_data = validate_optional_fields([optional_record, optional_record], config)
    valid_data.should.be.a(list)
    valid_data[0].should.be.a(dict)
    valid_data[0]['all_valid'].should.be.true
    for key in optional_fields:
        valid_data[0][key].should.be.true 
    
    valid_data[1].should.be.a(dict)
    valid_data[1]['all_valid'].should.be.true
    for key in optional_fields:
        valid_data[1][key].should.be.true


def test_validate_optional_fields_passes_none_values(optional_record):
    none_data = [optional_record, optional_record]
    none_data[0]['SchedLine'] = None 
    valid_data = validate_optional_fields(none_data, config)
    valid_data[0]['all_valid'].should.be.true
    valid_data[0]['SchedLine'].should.be.true

def test_validate_optional_fields_fails_with_incorrect_data_type(optional_record):
    wrong_data = [optional_record, optional_record] 
    # Should be a  string
    wrong_data[0]['SchedLine'] = 0
    # should be an integer
    wrong_data[0]['Input_Material_Lead_Time_cal_days'] = "5"
    # Should be a date
    wrong_data[0]['Input_Material_Order_Date'] = '2018-01-01'
    valid_data = validate_optional_fields(wrong_data, config)
    valid_data[0]['all_valid'].should.be.false
    valid_data[0]['SchedLine'].should.be.false
    valid_data[0]['Input_Material_Lead_Time_cal_days'].should.be.false
    valid_data[0]['Input_Material_Order_Date'].should.be.false

# Test utilities
def test_get_default_data_returns_correct_type():
    default_values = config['default_values']
    for data_type, value in default_values.items():
        get_default_data(data_type, config).should.be.a(type(value))

def test_default_values_fills_in_missing_data(valid_record):
    data = [deepcopy(valid_record), deepcopy(valid_record)]
    first_field = mandatory_fields[0]
    first_type = config['mandatory_fields'][first_field]
    first_expected = config['default_values'][first_type]
    data[0][first_field] = '' 
    second_field = mandatory_fields[1]
    second_type = config['mandatory_fields'][second_field]
    second_expected = config['default_values'][second_type]
    data[1][second_field] = '' 
    clean_data = set_default_values(data, config)
    clean_data[0][first_field].should.equal(first_expected)
    clean_data[1][second_field].should.equal(second_expected)

def test_fill_missing_values_replaces_empty_strings_with_none():
    data = [
        {'foo': '', 'bar': 'bar'},
        {'foo': 'foo', 'bar': ''}
    ]

    none_data = fill_missing_values(data)
    
    none_data[0]['foo'].should.equal(None)
    none_data[0]['bar'].should.equal('bar')
    none_data[1]['foo'].should.equal('foo')
    none_data[1]['bar'].should.equal(None)

def test_set_data_types_handles_integers_and_dates():
    data = [
        { 
            "Part_Material_Number_Buyer": "string",
            "Vendor_Code_Buyer_Supplier_Reference": "string",
            "Work_Production_Order_No_Supplier": "string",
            "Planned_Production_Start_Date": "2019-02-07T12:15:56",
            "Planned_Production_End_Date": "2019-02-07T12:15:56",
            "Planned_Production_Qty": "5.0",
            "Actual_Start_Production_Qty": "5.0",
            "Actual_End_Production_Qty": "5",
            "Work_Order_Status": "string",
            "Finished_Components_in_Storage_Qty": "5", 
            "Doc_Number_DemandReference_Buyer": "string",
            "SchedLine": "string",
            "Buyer_Plant_No": "string",
            "Assembly_Work_Order_Reference": "string",
            "Work_Order_Category": "string",
            "Current_Production_Step": "5.0",
            "TotalNumber_Production_Steps": "5.0",
            "Production_Lead_Time": "5.0",
            "Updated_Planned_Production_End_Date": "2019-02-07T12:15:56",
            "Actual_Production_Start_Date": "2019-02-07T12:15:56",
            "Actual_Production_End_Date": "2019-02-07T12:15:56",
            "Current_Work_Order_Qty": "5.0",
            "Finished_Components_in_Transit_Qty": "5.0",
            "Supplier_Input_Material_Qty": "5.0",
            "Supplier_Input_Material_on_Order_Qty": "5.0",
            "Input_Material_Lead_Time_cal_days": "5.0",
            "Input_Material_Order_Date": "2019-02-07T12:15:56",
            "Input_Material_Delivery_Date": "2019-02-07T12:15:56"
        },
        { 
            "Part_Material_Number_Buyer": "string",
            "Vendor_Code_Buyer_Supplier_Reference": "string",
            "Work_Production_Order_No_Supplier": "string",
            "Planned_Production_Start_Date": "2019-02-07T12:15:56",
            "Planned_Production_End_Date": "2019-02-07T12:15:56",
            "Planned_Production_Qty": "5.0",
            "Actual_Start_Production_Qty": "5.0",
            "Actual_End_Production_Qty": "5",
            "Work_Order_Status": "string",
            "Finished_Components_in_Storage_Qty": "5", 
            "Doc_Number_DemandReference_Buyer": "string",
            "SchedLine": "string",
            "Buyer_Plant_No": "string",
            "Assembly_Work_Order_Reference": "string",
            "Work_Order_Category": "string",
            "Current_Production_Step": "5.0",
            "TotalNumber_Production_Steps": "5.0",
            "Production_Lead_Time": "5.0",
            "Updated_Planned_Production_End_Date": "2019-02-07T12:15:56",
            "Actual_Production_Start_Date": "2019-02-07T12:15:56",
            "Actual_Production_End_Date": "2019-02-07T12:15:56",
            "Current_Work_Order_Qty": "5.0",
            "Finished_Components_in_Transit_Qty": "5.0",
            "Supplier_Input_Material_Qty": "5.0",
            "Supplier_Input_Material_on_Order_Qty": "5.0",
            "Input_Material_Lead_Time_cal_days": "5.0",
            "Input_Material_Order_Date": "2019-02-07T12:15:56",
            "Input_Material_Delivery_Date": "2019-02-07T12:15:56"
        }  
    ]

    type_data = set_data_types(data, config)
    type_data[0]['Planned_Production_Start_Date'].should.equal(datetime.date(2019, 2, 7))
    type_data[1]['Planned_Production_Start_Date'].should.equal(datetime.date(2019, 2, 7))
    type_data[0]['Updated_Planned_Production_End_Date'].should.equal(datetime.date(2019, 2, 7))
    type_data[1]['Updated_Planned_Production_End_Date'].should.equal(datetime.date(2019, 2, 7))
    type_data[0]['Planned_Production_Qty'].should.equal(5)
    type_data[1]['Planned_Production_Qty'].should.equal(5)
    type_data[0]['Finished_Components_in_Transit_Qty'].should.equal(5)
    type_data[1]['Finished_Components_in_Transit_Qty'].should.equal(5)
