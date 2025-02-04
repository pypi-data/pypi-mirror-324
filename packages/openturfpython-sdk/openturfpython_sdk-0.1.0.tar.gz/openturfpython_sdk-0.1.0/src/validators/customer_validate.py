from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date


class Address(BaseModel):
    Address1: Optional[str] = None
    Address2: Optional[str] = None
    City: Optional[str] = None
    PostalCode: Optional[str] = None
    HomeNumber: Optional[str] = None

class MailAddress(BaseModel):
    Address1: Optional[str] = None
    Address2: Optional[str] = None
    Address3: Optional[str] = None
    Address4: Optional[str] = None
    City: str
    State: str
    Country: str
    PostalCode: str
    WorkNumber: Optional[str] = None
    Extension: Optional[str] = None

class IdentificationType(BaseModel):
    IDType: str
    IDNumber: str
    IssueDate: Optional[str] = None
    ExpiryDate: Optional[str] = None
    CountryofIssue: str
    IDImage: Optional[str] = None
    IDImageName: Optional[str] = None


class CustomerInfo(BaseModel):
    Title: str = Field(..., max_length=5)
    FirstName: str = Field(..., max_length=25)
    LastName: str = Field(..., max_length=25)
    DOB: str = Field(..., pattern=r'^\d{8}$')  # DDMMYYYY
    MobileNumber: str = Field(..., pattern=r'^\+\d{1,15}$')  # Starts with + followed by up to 15 digits
    EmailAddress: EmailStr
    Address: Optional['Address'] = None
    MailAddress: Optional['MailAddress'] = None
    IdentificationType: Optional[List['IdentificationType']] = None
    FutureUse: Optional[dict] = None

class UpdateCustomerDetailsSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: str = Field(..., pattern=r'^\d{12,16}$')  # 12 or 16 digits
    CustomerInfo: CustomerInfo
    class Config:
        str_min_length = 1
        str_strip_whitespace = True

__all__ = ['UpdateCustomerDetailsSchema','CustomerInfo','IdentificationType','MailAddress','Address']