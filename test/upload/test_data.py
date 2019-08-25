from supplyon_uploader.uploader.data import get_data
from supplyon_uploader.uploader.data import get_data_type
from supplyon_uploader.uploader.data import validate_mandatory_fields
from supplyon_uploader.uploader.data import validate_optional_fields
import datetime
from pathlib import Path 
from copy import deepcopy

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

mandatory_fields = [
    'Part_Material_Number_Buyer',
    'Vendor_Code_Buyer_Supplier_Reference',
    'Work_Production_Order_No_Supplier',
    'Planned_Production_Start_Date',
    'Planned_Production_End_Date',
    'Actual_Production_Start_Date',
    'Actual_Production_End_Date',
    'Planned_Production_Qty',
    'Actual_Start_Production_Qty',
    'Current_Work_Order_Qty',
    'Work_Order_Status',
    'Finished_Components_in_Storage_Qty']

data = [
    {
        'Part_Material_Number_Buyer': 'string',
        'Vendor_Code_Buyer_Supplier_Reference': 'string',
        'Work_Production_Order_No_Supplier': 'string',
        'Planned_Production_Start_Date': datetime.datetime.now(),
        'Planned_Production_End_Date': datetime.datetime.now(),
        'Actual_Production_Start_Date': datetime.datetime.now(),
        'Actual_Production_End_Date': datetime.datetime.now(),
        'Planned_Production_Qty': 1,
        'Actual_Start_Production_Qty': 1,
        'Current_Work_Order_Qty': 1,
        'Work_Order_Status': 1,
        'Finished_Components_in_Storage_Qty': 1
    },
    {
        'Part_Material_Number_Buyer': 'string',
        'Vendor_Code_Buyer_Supplier_Reference': 'string',
        'Work_Production_Order_No_Supplier': 'string',
        'Planned_Production_Start_Date': datetime.datetime.now(),
        'Planned_Production_End_Date': datetime.datetime.now(),
        'Actual_Production_Start_Date': datetime.datetime.now(),
        'Actual_Production_End_Date': datetime.datetime.now(),
        'Planned_Production_Qty': 1,
        'Actual_Start_Production_Qty': 1,
        'Current_Work_Order_Qty': 1,
        'Work_Order_Status': 1,
        'Finished_Components_in_Storage_Qty': 1
    }
]

def test_validate_mandatory_fields_passes_valid_data():
    valid_data = validate_mandatory_fields(data)
    valid_data.should.be.a(list)
    valid_data[0].should.be.a(dict)
    valid_data[0]['all_valid'].should.be.true
    for key in mandatory_fields:
        valid_data[0][key].should.be.true 
    
    valid_data[1].should.be.a(dict)
    valid_data[1]['all_valid'].should.be.true
    for key in mandatory_fields:
        valid_data[1][key].should.be.true

def test_validate_mandatory_fields_fails_missing_field():
    missing_data = deepcopy(data)
    missing_data[0].pop('Part_Material_Number_Buyer')
    valid_data = validate_mandatory_fields(missing_data)
    valid_data[0]['all_valid'].should.be.false
    valid_data[0]['Part_Material_Number_Buyer'].should.be.false

def test_validate_mandatory_fields_fails_with_missing_data():
    missing_data = deepcopy(data)
    missing_data[0]['Part_Material_Number_Buyer'] = None
    valid_data = validate_mandatory_fields(missing_data)
    valid_data[0]['all_valid'].should.be.false
    valid_data[0]['Part_Material_Number_Buyer'].should.be.false

def test_validate_mandatory_fields_fails_wrong_type():
    missing_data = deepcopy(data)
    # This should be a string
    missing_data[0]['Part_Material_Number_Buyer'] = 0 
    # This should be a datetime.datetime
    missing_data[0]['Planned_Production_Start_Date'] = 0 
    # This should be an integer
    missing_data[0]['Current_Work_Order_Qty'] = '0' 

    valid_data = validate_mandatory_fields(missing_data)
    valid_data[0]['all_valid'].should.be.false
    valid_data[0]['Part_Material_Number_Buyer'].should.be.false
    valid_data[0]['Planned_Production_Start_Date'].should.be.false
    valid_data[0]['Current_Work_Order_Qty'].should.be.false

optional_fields = [
    'Doc_Number_DemandReference_Buyer',
    'SchedLine',
    'Buyer_Plant_No',
    'Current_Production_Step',
    'TotalNumber_Production_Steps',
    'Production_Lead_Time',
    'Updated_Planned_Production_End_Date',
    'Actual_End_Production_Qty',
    'Finished_Components_in_Transit_Qty',
    'Supplier_Input_Material_Qty',
    'Supplier_Input_Material_on_Order_Qty',
    'Input_Material_Lead_Time_cal_days',
    'Input_Material_Order_Date',
    'Input_Material_Delivery_Date'
]

optional_data = [
    {
        'Doc_Number_DemandReference_Buyer': 'string',
        'SchedLine': 'string',
        'Buyer_Plant_No': 'string',
        'Current_Production_Step': 1, 
        'TotalNumber_Production_Steps': 1,
        'Production_Lead_Time': 1,
        'Updated_Planned_Production_End_Date': datetime.datetime.now(),
        'Actual_End_Production_Qty': 1,
        'Finished_Components_in_Transit_Qty': 1,
        'Supplier_Input_Material_Qty': 1,
        'Supplier_Input_Material_on_Order_Qty': 1,
        'Input_Material_Lead_Time_cal_days': 1,
        'Input_Material_Order_Date': datetime.datetime.now(),
        'Input_Material_Delivery_Date': datetime.datetime.now()
    },
    {
        'Doc_Number_DemandReference_Buyer': 'string',
        'SchedLine': 'string',
        'Buyer_Plant_No': 'string',
        'Current_Production_Step': 1, 
        'TotalNumber_Production_Steps': 1,
        'Production_Lead_Time': 1,
        'Updated_Planned_Production_End_Date': datetime.datetime.now(),
        'Actual_End_Production_Qty': 1,
        'Finished_Components_in_Transit_Qty': 1,
        'Supplier_Input_Material_Qty': 1,
        'Supplier_Input_Material_on_Order_Qty': 1,
        'Input_Material_Lead_Time_cal_days': 1,
        'Input_Material_Order_Date': datetime.datetime.now(),
        'Input_Material_Delivery_Date': datetime.datetime.now()
    }
]

def test_validate_optional_fields_passes_valid_data():
    valid_data = validate_optional_fields(optional_data)
    valid_data.should.be.a(list)
    valid_data[0].should.be.a(dict)
    valid_data[0]['all_valid'].should.be.true
    for key in optional_fields:
        valid_data[0][key].should.be.true 
    
    valid_data[1].should.be.a(dict)
    valid_data[1]['all_valid'].should.be.true
    for key in optional_fields:
        valid_data[1][key].should.be.true


def test_validate_optional_fields_passes_none_values():
    none_data = deepcopy(optional_data)
    none_data[0]['SchedLine'] = None 
    valid_data = validate_optional_fields(none_data)
    valid_data[0]['all_valid'].should.be.true
    valid_data[0]['SchedLine'].should.be.true

def test_validate_optional_fields_fails_with_incorrect_data_type():
    wrong_data = deepcopy(optional_data)
    # Should be a  string
    wrong_data[0]['SchedLine'] = 0
    # should be an integer
    wrong_data[0]['Input_Material_Lead_Time_cal_days'] = "5"
    # Should be a date
    wrong_data[0]['Input_Material_Order_Date'] = '2018-01-01'
    valid_data = validate_optional_fields(wrong_data)
    valid_data[0]['all_valid'].should.be.false
    valid_data[0]['SchedLine'].should.be.false
    valid_data[0]['Input_Material_Lead_Time_cal_days'].should.be.false
    valid_data[0]['Input_Material_Order_Date'].should.be.false