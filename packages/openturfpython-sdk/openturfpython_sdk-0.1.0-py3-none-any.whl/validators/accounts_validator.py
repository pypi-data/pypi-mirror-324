from pydantic import BaseModel, Field,  EmailStr
import re
from typing import Optional, List
from pydantic import BaseModel, constr, condecimal, conlist, conint, Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from src.validators.common_validator import ProductInfoSchema

class AddAccountSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ProxyNumber: str = Field(..., max_length=16, description="ProxyNumber must be a string")
    ProductInfo: dict = Field(..., description="ProductInfo must be an object")

    class Config:
        str_min_length = 1
        str_strip_whitespace = True

class QueryBalanceSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ProxyNumber: str = Field(..., max_length=16, description="ProxyNumber must be a string")

class AmountRefundSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ProxyNumber: str = Field(..., max_length=16, description="ProxyNumber must be a string")
    ProductCode: str = Field(..., max_length=6, description="ProductCode must be a string")
    Amount: str = Field(..., max_length=12, description="Amount must be a string")
    RequestType: Optional[str] = Field(None, description="RequestType must be a string")

    @field_validator('Amount')
    def validate_amount(cls, value):
        if not re.match(r'^\d+(\.\d{1,2})?$', value):
            raise ValueError('Amount must be a valid number with up to 2 decimal places')
        return value

class AccountClosureSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ProxyNumber: str = Field(..., max_length=16, description="ProxyNumber must be a string")
    ProductCode: str = Field(..., max_length=6, description="ProductCode must be a string")

class DebitCreditAccountSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ProxyNumber: str = Field(..., max_length=16, description="ProxyNumber must be a string")
    ProductCode: str = Field(..., max_length=6, description="ProductCode must be a string")
    Type: str = Field(..., pattern=r'^[A-Za-z]{3}$', description="Type must be either BAT or FEE")
    Flag: str = Field(..., pattern=r'^[A-Za-z]{2}$', description="Flag must be either DR or CR")
    Amount: str = Field(..., max_length=12, description="Amount must be a string")
    Currency: str = Field(..., pattern=r'^[A-Z]{3}$', description="Currency must be a valid ISO 4217 currency code")
    Remarks: str = Field(..., max_length=250, description="Remarks are required")

    @field_validator('Amount')
    def validate_amount(cls, value):
        if not re.match(r'^\d+(\.\d{1,2})?$', value):
            raise ValueError('Amount must be a valid number with up to 2 decimal places')
        return value

    class Config:
        str_min_length = 1
        str_strip_whitespace = True


class SourceAccount(BaseModel):
    ProxyNumber: str = Field(..., max_length=16, description="SourceAccount.ProxyNumber must be a string")
    ProductCode: str = Field(..., length=6, description="SourceAccount.ProductCode must be exactly 6 characters long")
    AccountCcy: str = Field(..., length=3, pattern=r'^[A-Z]{3}$', description="SourceAccount.AccountCcy must be a valid ISO 4217 currency code")

class DestAccount(BaseModel):
    ProxyNumber: str = Field(..., max_length=16, description="DestAccount.ProxyNumber must be a string")
    ProductCode: str = Field(..., length=6, description="DestAccount.ProductCode must be exactly 6 characters long")
    AccountCcy: str = Field(..., length=3, pattern=r'^[A-Z]{3}$', description="DestAccount.AccountCcy must be a valid ISO 4217 currency code")
    Amount: str = Field(..., length=12, pattern=r'^\d+(\.\d{1,2})?$', description="DestAccount.Amount must be a valid number with up to 2 decimal places")

class FundTransferSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, pattern=r'^[a-zA-Z0-9]{12}$|^[a-zA-Z0-9]{32}$', description="TxnRefNo must be either 12 or 32 alphanumeric characters")
    ExchangeRate: Optional[str] = Field(None, max_length=12, pattern=r'^\d+(\.\d{1,6})?$', description="ExchangeRate must be a valid number with up to 6 decimal places")
    SourceAccount: SourceAccount
    DestAccount: DestAccount

class ExchangeRateDetailSchema(BaseModel):
    BuyCurrency: str = Field(..., length=3, pattern=r'^[A-Z]{3}$', description="BuyCurrency must be a valid ISO 4217 currency code")
    SellCurrency: str = Field(..., length=3, pattern=r'^[A-Z]{3}$', description="SellCurrency must be a valid ISO 4217 currency code")
    ExRate: str = Field(..., length=12, pattern=r'^\d+(\.\d{1,6})?$', description="ExRate must be a valid number with up to 6 decimal places")

class UpdateExchangeRateSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ExRates: List[ExchangeRateDetailSchema] = Field(..., min_items=1, description="ExRates must contain at least one exchange rate detail")

class ProfileCreationSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ProxyNumber: str = Field(..., max_length=16, description="ProxyNumber must be a string")
    UserId: str = Field(..., max_length=8, description="UserId must be a string")
    Password: str = Field(..., min_length=8, max_length=16, description="Password must be a string between 8 and 16 characters")
    EmailId: Optional[str] = Field(None, max_length=50, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="EmailId must be a valid email address")
    MobileNumber: Optional[str] = Field(None, max_length=15, pattern=r'^[\d\+]+$', description="MobileNumber must be a string containing digits and optional '+' sign")

class ChangePasswordSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Transaction Reference Number")
    OldPassword: str = Field(..., min_length=8, max_length=16, description="Old Password")
    NewPassword: str = Field(..., min_length=8, max_length=16, description="New Password")

    @field_validator('TxnRefNo')
    def txn_ref_no_max_length(cls, value):
        if len(value) > 32:
            raise ValueError('TxnRefNo must not exceed 32 characters')
        return value

class GetAccessRightsSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Transaction Reference Number")
    UserId: str = Field(..., min_length=8, max_length=8, description="User ID (exactly 8 characters)")

class PinRetrievalSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Transaction Reference Number")
    ProxyNumber: str = Field(..., max_length=16, description="Proxy Number")
    ExpiryDate: str = Field(..., pattern=r'^\d{2}\d{2}$', description="Expiry Date in MMYY format")
    CVV2: str = Field(..., pattern=r'^\d{3}$', description="3-digit CVV2 code")
    DOB: str = Field(..., pattern=r'^\d{2}\d{2}\d{4}$', description="Date of Birth in DDMMYYYY format")

    @field_validator('ExpiryDate')
    def expiry_date_format(cls, value):
        if not value.isdigit():
            raise ValueError('ExpiryDate must be numeric')
        if len(value) != 4:
            raise ValueError('ExpiryDate must be in MMYY format')
        return value

    @field_validator('CVV2')
    def cvv2_format(cls, value):
        if not value.isdigit():
            raise ValueError('CVV2 must be numeric')
        if len(value) != 3:
            raise ValueError('CVV2 must be exactly 3 digits')
        return value

    @field_validator('DOB')
    def dob_format(cls, value):
        if not value.isdigit():
            raise ValueError('DOB must be numeric')
        if len(value) != 8:
            raise ValueError('DOB must be in DDMMYYYY format')
        return value


class AtmPinVerificationSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ProxyNumber: str = Field(..., max_length=16, description="ProxyNumber must be a string")
    EPinBlock: str = Field(..., length=16, description="EPinBlock must be a 16-character hexadecimal string")
    DOB: str = Field(..., length=8, description="DOB must be in DDMMYYYY format")

    @field_validator('EPinBlock')
    def validate_pin_block(cls, value):
        if not re.match(r'^[0-9A-Fa-f]{16}$', value):
            raise ValueError('EPinBlock must be a 16-character hexadecimal string')
        return value

    @field_validator('DOB')
    def validate_dob(cls, value):
        if not re.match(r'^\d{2}\d{2}\d{4}$', value):
            raise ValueError('DOB must be in DDMMYYYY format')
        return value


class AtmPinChangeSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ProxyNumber: str = Field(..., max_length=16, description="ProxyNumber must be a string")
    EoldPinBlock: str = Field(..., length=16, description="EoldPinBlock must be a 16-character hexadecimal string")
    EnewPinBlock: str = Field(..., length=16, description="EnewPinBlock must be a 16-character hexadecimal string")

    @field_validator('EoldPinBlock', 'EnewPinBlock')
    def validate_pin_block(cls, value):
        if not re.match(r'^[0-9A-Fa-f]{16}$', value):
            raise ValueError('PinBlock must be a 16-character hexadecimal string')
        return value

class AssignOverrideSettingsSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ProxyNumber: str = Field(..., max_length=16, description="ProxyNumber must be a string")
    CampaignCode: str = Field(..., max_length=10, description="CampaignCode must be a string")
    ProductCode: str = Field(..., length=6, description="ProductCode must be a 6-character string")
    Flag: str = Field(..., length=1, pattern=r'^[YN]$', description="Flag must be either 'Y' or 'N'")

# Alert Setting Schema
class AlertSettingSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="TxnRefNo must be a string")
    ProxyNumber: str = Field(..., max_length=16, description="ProxyNumber must be a string")
    ProductCode: str = Field(..., length=6, description="ProductCode must be a 6-character string")
    AlertType: str = Field(..., length=6, pattern=r'^(ATMCWD|PURCSE|LOWBAL|TOPACC)$', description="AlertType must be one of 'ATMCWD', 'PURCSE', 'LOWBAL', 'TOPACC'")
    Frequency: str = Field(..., length=3, pattern=r'^(DLY|WLY|MLY|YLY|TXN)$', description="Frequency must be one of 'DLY', 'WLY', 'MLY', 'YLY', 'TXN'")
    AlertData: Optional[str] = Field(None, length=12, pattern=r'^\d{12}$', description="AlertData must be a 12-digit string")
    Channel: str = Field(..., length=5, pattern=r'^(SMS|EMAIL|BOTH)$', description="Channel must be either 'SMS', 'EMAIL', or 'BOTH'")
    AlertSet: str = Field(..., length=1, pattern=r'^[YN]$', description="AlertSet must be either 'Y' or 'N'")

    @field_validator('AlertData')
    def validate_alert_data(cls, value):
        if value and not re.match(r'^\d{12}$', value):
            raise ValueError('AlertData must be exactly 12 digits')
        return value
    

class ResetWebPasswordSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32, description="Unique Transaction Reference generated by Service Requestor")
    Reftext1: Optional[str] = Field(None, max_length=100, description="Optional future use text 1")
    Reftext2: Optional[str] = Field(None, max_length=100, description="Optional future use text 2")
    Reftext3: Optional[str] = Field(None, max_length=100, description="Optional future use text 3")
    NewPassword: str = Field(..., min_length=8, max_length=16, description="New Password should be between 8 and 16 characters")
    ConfirmPassword: str = Field(..., min_length=8, max_length=16, description="Confirm Password should be between 8 and 16 characters")

    @field_validator('TxnRefNo')
    def txn_ref_no_max_length(cls, v: str) -> str:
        if len(v) > 32:
            raise ValueError('TxnRefNo must not exceed 32 characters')
        return v

    @field_validator("ConfirmPassword", mode="after")
    def password_match(cls, v: str, info: ValidationInfo) -> str:
        new_password = info.data.get("NewPassword")
        if new_password and v != new_password:
            raise ValueError("NewPassword and ConfirmPassword must match")
        return v


class AtmPinSetSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: str = Field(..., max_length=16)
    ExpiryDate: str = Field(..., pattern=r"^(0[1-9]|1[0-2])([0-9]{2})$", description="Expiry Date of the Card Front panel in MMYY format")
    CVV2: Optional[str] = Field(None, pattern=r"^\d{3}$")
    DOB: str = Field(..., pattern=r"^(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])(\d{4})$")
    EPinBlock: str = Field(..., max_length=16)

# OTP Request Schema
class NewOTPRequestSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: str = Field(..., max_length=16)
    ExpiryDate: Optional[str] = Field(None, min_length=4, max_length=4)
    Reftext1: Optional[str] = Field(None, max_length=25)
    Reftext2: Optional[str] = Field(None, max_length=25)
    Reftext3: Optional[str] = Field(None, max_length=25)


class OTPValidationSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: str = Field(..., max_length=16)
    OTP: str = Field(..., min_length=6, max_length=6, pattern=r"^\d+$")

class RetrieveWebProfileSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    ProxyNumber: str = Field(...)
    Reftext1: Optional[str] = Field(None, max_length=100)
    Reftext2: Optional[str] = Field(None, max_length=100)
    Reftext3: Optional[str] = Field(None, max_length=100)


class CorporateRegistrationSchema(BaseModel):
    TxnRefNo: str = Field(..., max_length=32)
    CorpNameOne: str = Field(..., max_length=100)
    CorpNameTwo: Optional[str] = Field(None, max_length=100)
    CorpNameThree: Optional[str] = Field(None, max_length=100)
    StreetName: str = Field(..., max_length=100)
    City: str = Field(..., max_length=50)
    Country: str = Field(..., max_length=30)
    PostalCode: Optional[str] = Field(None, max_length=8)
    CorporateId: Optional[str] = Field(None, min_length=10, max_length=10)
    CrmId: Optional[str] = Field(None, max_length=20)
    CorporateLoginId: str = Field(..., min_length=10, max_length=10)
    EnterpriseId: Optional[str] = Field(None, max_length=50)
    TaxNumber: Optional[str] = Field(None, max_length=15)
    PrintName: Optional[str] = Field(None, max_length=20)
    Optional1: Optional[str] = Field(None, max_length=100)
    Optional2: Optional[str] = Field(None, max_length=100)
    Optional3: Optional[str] = Field(None, max_length=100)
    
    class CorporateContact(BaseModel):
        Gender: str = Field(..., min_length=1, max_length=1, pattern=r'^[MF]$')
        Title: Optional[str] = Field(None, max_length=25)
        FirstName: Optional[str] = Field(None, max_length=30)
        LastName: str = Field(..., max_length=30)
        MailAddress: Optional[str] = Field(None, max_length=100)
        OfficePhone: Optional[str] = Field(None, max_length=20)
        ResidentPhone: Optional[str] = Field(None, pattern=r'^\d+(-\d+)*$', max_length=20)
        Mobile: Optional[str] = Field(None, pattern=r'^\d+(-\d+)*$', max_length=20)
        Fax: Optional[str] = Field(None, pattern=r'^\d+(-\d+)*$', max_length=20)
        Suburb: Optional[str] = Field(None, max_length=30)
        State: Optional[str] = Field(None, max_length=30)
        Country: Optional[str] = Field(None, max_length=30)
        EmailId: EmailStr = Field(..., max_length=100)

    corporate_contact: CorporateContact
    PostalCode: Optional[str] = Field(None, max_length=8)


__all__ = ['CorporateRegistrationSchema']