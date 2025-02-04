from typing import Optional
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal

class ProductInfoSchema(BaseModel):
    # String with a maximum length of 6
    ProductCode: str = Field(..., max_length=6)
    
    # Decimal with max_digits=12 and decimal_places=2
    LoadAmount: Decimal = Field(..., max_digits=12, decimal_places=2)
    
    BillingAmount: Decimal = Field(..., max_digits=12, decimal_places=2)
    
    # String with pattern to match 3 uppercase letters
    LoadCurrency: str = Field(..., pattern=r'^[A-Z]{3}$')  # 3 uppercase letters
    BillingCurrency: str = Field(..., pattern=r'^[A-Z]{3}$')  # 3 uppercase letter

    class Config:
        str_min_length = 1
        str_strip_whitespace = True


class AddressSchema(BaseModel):
    Address1: Optional[str] = None
    Address2: Optional[str] = None
    Address3: Optional[str] = None
    Address4: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Country: Optional[str] = None
    PostalCode: Optional[str] = None
    HomeNumber: Optional[str] = None


address = AddressSchema()


class MailAddressSchema(AddressSchema):
    WorkNumber: Optional[str] = None
    Extension: Optional[str] = None


class IdentificationTypeSchema(BaseModel):
    IDType: str
    IDNumber: str
    ExpiryDate: Optional[str] = Field(None, pattern=r'^\d{8}$')  # Validates 8 digits for the expiry date
    CountryofIssue: str

class CustomerInfoSchema(BaseModel):
    Title: str = Field(..., max_length=5)  # String with a max length of 5
    FirstName: str = Field(..., max_length=25)  # String with a max length of 25
    LastName: str = Field(..., max_length=25)  # String with a max length of 25
    DOB: str = Field(..., pattern=r'^\d{8}$')  # Date of birth in the format YYYYMMDD (8 digits)
    Gender: str = Field(..., pattern=r'^(M|F)$')  # Gender is either M or F
    MobileNumber: str = Field(..., pattern=r'^\+\d{1,15}$')  # Mobile number with country code
    EmailAddress: str = Field(..., max_length=50, pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')  # Valid email format
    Image: Optional[str] = None  # Optional image URL or identifier
    Address: 'AddressSchema'  # Assuming AddressSchema is defined elsewhere
    MailAddress: 'MailAddressSchema'  # Assuming MailAddressSchema is defined elsewhere
    IdentificationType: Optional[List[IdentificationTypeSchema]] = None  # List of Identification Types, optional with at least one item


    class Config:
        str_strip_whitespace = True
        str_min_length = 1
