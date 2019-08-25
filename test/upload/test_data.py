from supplyon_uploader.uploader.data import get_data
from supplyon_uploader.uploader.data import get_data_type
from supplyon_uploader.uploader.data import validate_mandatory_fields
import datetime
from pathlib import Path 

test_data_path = Path('.').absolute() /'test/data/test_data.csv'

def test_get_data_returns_a_list_of_dicts():
    data = get_data(test_data_path)
    data.should.be.a(list)
    for row in data:
        row.should.be.a(dict)

def test_get_data_type_handles_string():
    get_data_type("string")().should.be.a(str)


def test_get_data_type_handles_int():
    get_data_type("integer")().should.be.a(int)

def test_get_data_type_handles_date():
    get_data_type("date").now().should.be.a(datetime.datetime)

def test_get_data_invalid_descriptions_return_false():
    get_data_type("str").should.be.false
    get_data_type(str).should.be.false
    get_data_type(datetime).should.be.false

mandatory_fields = [
    "Part_Material_Number_Buyer",
    "Vendor_Code_Buyer_Supplier_Reference",
    "Work_Production_Order_No_Supplier",
    "Planned_Production_Start_Date",
    "Planned_Production_End_Date",
    "Actual_Production_Start_Date",
    "Actual_Production_End_Date",
    "Planned_Production_Qty",
    "Actual_Start_Production_Qty",
    "Current_Work_Order_Qty",
    "Work_Order_Status",
    "Finished_Components_in_Storage_Qty"]

data = [
    {
        "Part_Material_Number_Buyer": "string",
        "Vendor_Code_Buyer_Supplier_Reference": "string",
        "Work_Production_Order_No_Supplier": "string",
        "Planned_Production_Start_Date": datetime.datetime.now(),
        "Planned_Production_End_Date": datetime.datetime.now(),
        "Actual_Production_Start_Date": datetime.datetime.now(),
        "Actual_Production_End_Date": datetime.datetime.now(),
        "Planned_Production_Qty": 1,
        "Actual_Start_Production_Qty": 1,
        "Current_Work_Order_Qty": 1,
        "Work_Order_Status": 1,
        "Finished_Components_in_Storage_Qty": 1
    },
    {
        "Part_Material_Number_Buyer": "string",
        "Vendor_Code_Buyer_Supplier_Reference": "string",
        "Work_Production_Order_No_Supplier": "string",
        "Planned_Production_Start_Date": datetime.datetime.now(),
        "Planned_Production_End_Date": datetime.datetime.now(),
        "Actual_Production_Start_Date": datetime.datetime.now(),
        "Actual_Production_End_Date": datetime.datetime.now(),
        "Planned_Production_Qty": 1,
        "Actual_Start_Production_Qty": 1,
        "Current_Work_Order_Qty": 1,
        "Work_Order_Status": 1,
        "Finished_Components_in_Storage_Qty": 1
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




