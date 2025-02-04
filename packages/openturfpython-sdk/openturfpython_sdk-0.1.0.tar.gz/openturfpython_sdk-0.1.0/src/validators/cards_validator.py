from __future__ import print_function
from pydantic import BaseModel, Field, root_validator
from typing import Optional, Literal, List
from datetime import datetime
from pydantic import BaseModel, Field, constr, field_validator
from typing import Optional, Literal
import re
import jsonschema
from src.utils import *

card_schema = {
    "type": "object",
    "properties": {
        "cardNumber": {"type": "string"},
        "expiryDate": {"type": "string"},
        "cvv": {"type": "string"}
    },
    "required": ["cardNumber", "expiryDate", "cvv"]
}

def validate_card_details(card_details):
    try:
        jsonschema.validate(instance=card_details, schema=card_schema)  
    except jsonschema.exceptions.ValidationError as e:
        raise Exception(str(e))
    
    
class GetCardDetailSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Transaction Reference Number is required and must not exceed 32 characters.")
    ProxyNumber: str = Field(..., max_length=16, description="Proxy Number is required and must not exceed 16 characters.")
    CustomerId: Optional[str] = Field(None, max_length=100, description="Customer ID must not exceed 100 characters.")

class LoadDetailsSchema(BaseModel):
    ProductCode: str = Field(..., max_length=6, description="Product Code is required and must be at most 6 characters long.")
    LoadAmount: str = Field(..., max_length=12, description="Load Amount is required and must be at most 12 characters long.")
    BillingAmount: str = Field(..., max_length=12, description="Billing Amount is required and must be at most 12 characters long.")
    LoadCurrency: str = Field(..., max_length=3, description="Load Currency is required and must be at most 3 characters long.")
    BillingCurrency: str = Field(..., max_length=3, description="Billing Currency is required and must be at most 3 characters long.")

class GetNewCardSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: Optional[str] = Field(None, max_length=16)
    CustomerId: Optional[str] = Field(None, max_length=100)
    NameOnCard: Optional[str] = Field(None, max_length=25)
    CardDesign: Optional[str] = Field(None, max_length=6)
    CardActivationFlag: Optional[str] = Field(None, max_length=1)
    AlertFlag: Optional[str] = Field(None, max_length=1)
    RefText1: Optional[str] = Field(None, max_length=32)
    RefText2: Optional[str] = Field(None, max_length=6)
    RefText3: Optional[str] = Field(None, max_length=32)
    RefText4: Optional[str] = Field(None, max_length=32)
    CustomerInfo: Optional[dict] = None
    LoadDetails: Optional[LoadDetailsSchema] = None

class BlockLockUnlockCardSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: str = Field(..., max_length=16)
    Flag: Literal["BL", "BS", "BD", "L", "UL"]
    Reason: str = Field(..., max_length=25)

class CardActivationSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: str = Field(..., max_length=16)
    ActivationCode: Optional[str] = Field(None, max_length=6)
    CustomerId: Optional[str] = Field(None, max_length=100)

class CardReplacementSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: str = Field(..., max_length=16)
    NewProxyNumber: Optional[str] = Field(None, max_length=16)
    CustomerId: Optional[str] = Field(None, max_length=100)
    Type: Literal["VP", "PP"]
    CardDesign: Optional[str] = Field(None, max_length=6)
    DeliveryFlag: Optional[Literal["B", "C"]] = Field(None)

class LoadCardSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: str = Field(..., max_length=16)
    ProductInfo: Optional[dict] = None

class GetXTransactionsSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: str = Field(..., max_length=16)
    FromDate: str = Field(..., pattern=r"^\d{2}\d{2}\d{4}$", description="Must be in format DDMMYYYY")
    ToDate: str = Field(..., pattern=r"^\d{2}\d{2}\d{4}$", description="Must be in format DDMMYYYY")
    # Count: str = Field(..., max_length=2, pattern=r"^(\*\*|\d{1,2})$", description="Must be a valid number <= 99 or '**'.")
    Count: str = Field(..., max_length=2, pattern=r"^(\*\*|\d{1,2})$")
    PageNumber: Optional[str] = Field(None, max_length=2, pattern=r"^\d{1,2}$")

class PackNoSchema(BaseModel):
    PackNo: str = Field(
        ...,
        max_length=12,
        title="Pack Number",
        description="PackNo must be a string with a maximum of 12 characters."
    )

class UpdateStockDetailsSchema(BaseModel):
    TxnRefNo: str = Field(
        ...,
        max_length=32,
        title="Transaction Reference Number",
        description="TxnRefNo must not exceed 32 characters."
    )
    OrderRefNo: str = Field(
        ...,
        max_length=12,
        title="Order Reference Number",
        description="OrderRefNo must not exceed 12 characters."
    )
    Quantity: str = Field(
    ...,
    max_length=10,
    pattern=r'^\d+$',  # Changed `pattern` to `pattern`
    title="Quantity",
    description="Quantity must be a string with digits only and not exceed 10 characters."
)

    RefNumbers: List[PackNoSchema] = Field(
        ...,
        min_items=1,
        title="Reference Numbers",
        description="RefNumbers must contain at least one PackNo."
    )

# Card Receipt Schema
class ReceiptSchema(BaseModel):
    OrderRefNo: str = Field(
        ...,
        max_length=10,
        title="Order Reference Number",
        description="OrderRefNo must be a string with a maximum of 10 characters."
    )
    Quantity: str = Field(
    ...,
    max_length=10,
    pattern=r'^\d+$',  
    title="Quantity",
    description="Quantity must be a string with digits only and not exceed 10 characters."
)

    FromPackNo: str = Field(
        ...,
        max_length=12,
        title="From Pack Number",
        description="FromPackNo must be a string with a maximum of 12 characters."
    )
    ToPackNo: str = Field(
        ...,
        max_length=12,
        title="To Pack Number",
        description="ToPackNo must be a string with a maximum of 12 characters."
    )

class CardReceiptSchema(BaseModel):
    TxnRefNo: str = Field(
        ...,
        max_length=32,
        title="Transaction Reference Number",
        description="TxnRefNo must not exceed 32 characters."
    )
    Receipt: ReceiptSchema = Field(...)

# Card Order Schema
class DeliverySchema(BaseModel):
    Name: str = Field(
        ...,
        max_length=50,
        title="Delivery Name",
        description="Delivery.Name must be a string with a maximum of 50 characters."
    )
    Address1: str = Field(
        ...,
        max_length=35,
        title="Address Line 1",
        description="Delivery.Address1 must not exceed 35 characters."
    )
    Address2: str = Field(
        ...,
        max_length=35,
        title="Address Line 2",
        description="Delivery.Address2 must not exceed 35 characters."
    )
    Address3: Optional[str] = Field(
        None,
        max_length=35,
        title="Address Line 3",
        description="Delivery.Address3 is optional and must not exceed 35 characters."
    )
    Address4: Optional[str] = Field(
        None,
        max_length=35,
        title="Address Line 4",
        description="Delivery.Address4 is optional and must not exceed 35 characters."
    )
    City: str = Field(
        ...,
        max_length=20,
        title="City",
        description="Delivery.City must not exceed 20 characters."
    )
    State: str = Field(
        ...,
        max_length=20,
        title="State",
        description="Delivery.State must not exceed 20 characters."
    )
    Country: str = Field(
        ...,
        max_length=20,
        title="Country",
        description="Delivery.Country must not exceed 20 characters."
    )
    PostalCode: str = Field(
        ...,
        max_length=15,
        title="Postal Code",
        description="Delivery.PostalCode must not exceed 15 characters."
    )

class OrderSchema(BaseModel):
    BranchId: Optional[str] = Field(
        None,
        max_length=8,
        title="Branch ID",
        description="BranchId must not exceed 8 characters and can be optional."
    )
    ProductCode: str = Field(
        ...,
        max_length=6,
        title="Product Code",
        description="ProductCode must be a string and not exceed 6 characters."
    )
    CardDesign: str = Field(
        ...,
        max_length=6,
        title="Card Design",
        description="CardDesign must not exceed 6 characters."
    )
    Quantity: str = Field(
    ...,
    max_length=10,
    pattern=r'^\d+$',  # Changed `pattern` to `pattern`
    title="Quantity",
    description="Quantity must be digits only and not exceed 10 characters."
)

    Delivery: Optional[DeliverySchema] = Field(None)

class CardOrderSchema(BaseModel):
    TxnRefNo: str = Field(
        ...,
        max_length=32,
        title="Transaction Reference Number",
        description="TxnRefNo must not exceed 32 characters."
    )
    Order: OrderSchema = Field(...)


class PackNoSchema(BaseModel):
    PackNo: str = Field(
        ..., max_length=12,
        description="PackNo must be a string with a maximum length of 12 characters"
    )

    @field_validator('PackNo')
    def validate_pack_no(cls, value):
        if not isinstance(value, str):
            raise ValueError('PackNo must be a string')
        return value

class ReceiptSchema(BaseModel):
    OrderRefNo: str = Field(
        ..., max_length=10,
        description="OrderRefNo must be a string with a maximum length of 10 characters"
    )
    Quantity: str = Field(
        ..., max_length=10,
        description="Quantity must be a string with a maximum length of 10 characters"
    )
    FromPackNo: str = Field(
        ..., max_length=12,
        description="FromPackNo must be a string with a maximum length of 12 characters"
    )
    ToPackNo: str = Field(
        ..., max_length=12,
        description="ToPackNo must be a string with a maximum length of 12 characters"
    )

    @field_validator('Quantity')
    def validate_quantity(cls, value):
        if not value.isdigit():
            raise ValueError('Quantity must contain digits only')
        return value

class CardReceiptSchema(BaseModel):
    TxnRefNo: str = Field(
        ..., max_length=32,
        description="TxnRefNo must be a string with a maximum length of 32 characters"
    )
    Receipt: ReceiptSchema

    @field_validator('TxnRefNo')
    def validate_txn_ref_no(cls, value):
        if not isinstance(value, str):
            raise ValueError('TxnRefNo must be a string')
        return value

class UpdateStockDetailsSchema(BaseModel):
    TxnRefNo: str = Field(
        ..., max_length=32,
        description="TxnRefNo must be a string with a maximum length of 32 characters"
    )
    OrderRefNo: str = Field(
        ..., max_length=12,
        description="OrderRefNo must be a string with a maximum length of 12 characters"
    )
    Quantity: str = Field(
        ..., max_length=10,
        description="Quantity must be a string with a maximum length of 10 characters"
    )
    RefNumbers: List[PackNoSchema] = Field(
        ..., min_items=1,
        description="RefNumbers must be an array containing at least one PackNo"
    )

    @field_validator('Quantity')
    def validate_quantity(cls, value):
        if not value.isdigit():
            raise ValueError('Quantity must contain digits only')
        return value

    @field_validator('TxnRefNo', 'OrderRefNo')
    def validate_strings(cls, value):
        if not isinstance(value, str):
            raise ValueError(f'{value} must be a string')
        return value

# Custom pattern for validating DDMMYYYY and MMYY formats
DOB_pattern = r"^(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])\d{4}$"
EXPIRY_pattern = r"^(0[1-9]|1[0-2])\d{2}$"

class GetStockDetailsSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Unique Transaction Reference")
    BranchId: str = Field(..., max_length=8, description="Branch Identifier")

class StatusRequestSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Unique Transaction Reference")

class GetCardNumberSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Unique Transaction Reference generated by Service Requestor")
    ProxyNumber: str = Field(..., max_length=16, description="Either Source Card Number or Proxy Number")
    Reftext1: Optional[str] = Field(None, description="Future Use, client-specific.")
    Reftext2: Optional[str] = Field(None, description="Future Use")
    Reftext3: Optional[str] = Field(None, description="Future Use")

class GetCSCEnquirySchema(BaseModel):
    TxnRefNo: str = Field(
        ..., max_length=32, 
        description="Unique Transaction Reference generated by Service Requestor"
    )
    ProxyNumber: str = Field(
        ..., max_length=16, 
        description="Either Source Card Number (16 digits) or Proxy Number (12 digits)"
    )
    ExpiryDate: str = Field(
        ..., min_length=4, max_length=4, 
        pattern=EXPIRY_pattern,  # Changed `pattern` to `pattern`
        description="Expiry Date in MMYY format"
    )
    @field_validator("ExpiryDate")
    def validate_expiry_date(cls, value):
        if not re.match(EXPIRY_pattern, value):
            raise ValueError("ExpiryDate must be in MMYY format")
        return value

class GetCardOrderStatusSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Unique Transaction Reference generated by Service Requestor")
    InvoiceNo: str = Field(..., max_length=13, description="Either Invoice Number or Order Reference Number")

class IvrPinSetSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Unique Transaction Reference generated by Service Requestor")
    ProxyNumber: str = Field(..., max_length=16, description="Proxy Number")
    IvrPin: str = Field(..., min_length=6, max_length=6, description="IVR Pin should be exactly 6 characters")
    DOB: str = Field(
    ..., min_length=8, max_length=8, 
    pattern=r"^\d{8}$",  # Changed `pattern` to `pattern`
    description="Customer’s Date of Birth in DDMMYYYY format"
)

    @field_validator("DOB")
    def validate_dob(cls, value):
        if not re.match(r"^\d{8}$", value):
            raise ValueError("DOB must be in DDMMYYYY format")
        return value

class LoadDetails(BaseModel):
    ProductCode: str = Field(..., max_length=6, description="Product code must be exactly 6 characters long")
    LoadAmount: str = Field(..., max_length=12, description="Load amount must be less than or equal to 12 characters")
    BillingAmount: str = Field(..., max_length=12, description="Billing amount must be less than or equal to 12 characters")
    LoadCurrency: str = Field(..., max_length=3, description="Load currency must be exactly 3 characters long")
    BillingCurrency: str = Field(..., max_length=3, description="Billing currency must be exactly 3 characters long")

class AddCardSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Transaction reference number must not exceed 32 characters")
    ProxyNumber: str = Field(..., max_length=16, description="Proxy number must not exceed 16 characters")
    NewProxyNumber: Optional[str] = Field(None, max_length=16, description="New proxy number must not exceed 16 characters")
    CustomerId: str = Field(..., max_length=100, description="Customer ID must not exceed 100 characters")
    NameOnCard: Optional[str] = Field(None, max_length=25, description="Name on card must not exceed 25 characters")
    AddCardFlag: str = Field(..., description="AddCardFlag must be one of 'S' or 'A'")
    CardDesign: Optional[str] = Field(None, max_length=6, description="Card design must be exactly 6 characters long")
    CardActivationFlag: Optional[str] = Field(None, description="Card activation flag must be either 'Y' or 'N'")
    RefText1: Optional[str] = Field(None, max_length=32, description="RefText1 must not exceed 32 characters")
    RefText2: Optional[str] = Field(None, max_length=32, description="RefText2 must not exceed 32 characters")
    RefText3: Optional[str] = Field(None, max_length=32, description="RefText3 must not exceed 32 characters")
    RefText4: Optional[str] = Field(None, max_length=32, description="RefText4 must not exceed 32 characters")
    LoadDetails: LoadDetails

class IVRPinChangeSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Transaction reference number must not exceed 32 characters")
    ProxyNumber: str = Field(..., max_length=16, description="Proxy number must not exceed 16 characters")
    oldIvrPin: str = Field(..., max_length=16, description="Old IVR Pin must not exceed 16 characters")
    NewIvrPin: str = Field(..., max_length=16, description="New IVR Pin must not exceed 16 characters")

class IVRPinValidationSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Transaction reference number must not exceed 32 characters")
    ProxyNumber: str = Field(..., max_length=16, description="Proxy number must not exceed 16 characters")
    IvrPin: str = Field(..., min_length=6, max_length=6, description="IVR Pin must be exactly 6 characters long")
    DOB: Optional[str] = Field(
    None, min_length=8, max_length=8, 
    pattern=DOB_pattern,  # Changed `pattern` to `pattern`
    description="Date of birth in DDMMYYYY format"
)


__all__ = ['Field', 'BaseModel', 'GetCardDetailSchema', 'LoadDetailsSchema', 'GetNewCardSchema', 'BlockLockUnlockCardSchema', 'CardActivationSchema', 'CardReplacementSchema', 'LoadCardSchema', 'GetXTransactionsSchema', 'PackNoSchema', 'UpdateStockDetailsSchema', 'ReceiptSchema', 'CardReceiptSchema', 'DeliverySchema', 'OrderSchema', 'CardOrderSchema', 'PackNoSchema', 'ReceiptSchema', 'CardReceiptSchema', 'UpdateStockDetailsSchema', 'GetStockDetailsSchema', 'StatusRequestSchema', 'GetCardNumberSchema', 'GetCSCEnquirySchema', 'GetCardOrderStatusSchema', 'IvrPinSetSchema', 'LoadDetails', 'AddCardSchema', 'IVRPinChangeSchema', 'IVRPinValidationSchema']
