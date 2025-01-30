from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, ClassVar
from .data_types import Date
from decimal import Decimal, ROUND_HALF_UP
from .utils import fix_date_fields, convert_camel_to_snake
import re


class CustomBaseModel(BaseModel):
    rounding_fields: ClassVar[set[str]] = set()
    date_fields: ClassVar[set[str]] = set()

    @staticmethod
    def clean_price(value: str | float | int) -> Decimal:
        if isinstance(value, str):
            clean_value = re.sub(r"[^\d.]", "", value)
            try:
                return Decimal(clean_value)
            except Exception as e:
                raise ValueError(f"Invalid value for price: {value}") from e
        elif isinstance(value, (float, int)):
            return Decimal(str(value))
        return value

    @model_validator(mode="before")
    @classmethod
    def apply_transformations(cls, values):

        transformed_values = convert_camel_to_snake(values)

        for field in cls.rounding_fields:
            if field in transformed_values and transformed_values[field] is not None:
                cleaned_value = cls.clean_price(transformed_values[field])
                transformed_values[field] = cleaned_value.quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )

        for field in cls.date_fields:
            if field in transformed_values and transformed_values[field] is not None:
                transformed_values[field] = fix_date_fields(transformed_values[field])

        return transformed_values

    model_config = {
        "populate_by_name": True,
        "str_strip_whitespace": True,
    }


class Person(CustomBaseModel):
    tahoeId: Optional[str] = Field(None, max_length=50, alias="tahoe_id")
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[Date] = None
    is_decedent: Optional[bool] = False
    date_of_death: Optional[Date] = None
    person_type: Optional[str] = Field(
        "Owner", max_length=50, pattern="^(Owner|Relative|Neighbor|Associate)$"
    )
    relationship_to_owner: Optional[str] = Field(None, max_length=50)
    phone_numbers : Optional[list] = []
    emails : Optional[list] = []
    addresses : Optional[list] = []
    date_fields: ClassVar[set[str]] = {"date_of_birth", "date_of_death"}


class Auction(CustomBaseModel):
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    date: Optional[Date] = None
    opening_bid: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    link: Optional[str] = None
    rounding_fields: ClassVar[set[str]] = {"amount", "opening_bid"}
    date_fields: ClassVar[set[str]] = {"date"}


class Sale(CustomBaseModel):
    sale_date: Optional[Date] = None
    sale_amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    sale_status: Optional[str] = None
    nos_amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    rounding_fields: ClassVar[set[str]] = {"sale_amount", "nos_amount"}
    date_fields: ClassVar[set[str]] = {"sale_date"}


class Debt(CustomBaseModel):
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    rounding_fields: ClassVar[set[str]] = {"amount"}

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"


class LegalProceeding(CustomBaseModel):
    trustee_name: Optional[str] = None
    trustee_phone: Optional[str] = None
    trustee_sale_number: Optional[str] = None
    final_judgment: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    plaintiff: Optional[str] = None
    attorney_name: Optional[str] = None
    attorney_phone: Optional[str] = None
    attorney_bar_no: Optional[str] = None
    attorney_firm: Optional[str] = None
    defendants: Optional[str] = None
    total_amount_owed: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    document_name: Optional[str] = None
    case_number: Optional[str] = None
    case_type: Optional[str] = None
    date_of_filing: Optional[Date] = None
    probate_case_number: Optional[str] = None
    rounding_fields: ClassVar[set[str]] = {"final_judgment", "total_amount_owed"}
    date_fields: ClassVar[set[str]] = {"date_of_filing"}


class Mortgage(CustomBaseModel):
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    interest_rate: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    recording_date: Optional[int] = None
    document_date: Optional[int] = None
    maturity_date: Optional[int] = None
    document_number: Optional[str] = Field(None, max_length=50)
    recording_book: Optional[str] = Field(None, max_length=50)
    recording_page: Optional[str] = Field(None, max_length=50)
    lender_name: Optional[str] = Field(None, max_length=255)
    term_type: Optional[str] = Field(None, max_length=50)
    term: Optional[str] = Field(None, max_length=50)
    document_code: Optional[str] = Field(None, max_length=50)
    transaction_type: Optional[str] = Field(None, max_length=255)
    grantee_name: Optional[str] = Field(None, max_length=255)
    riders: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    position: Optional[str] = Field(None, max_length=50)
    term_description: Optional[str] = Field(None, max_length=255)
    loan_type: Optional[str] = Field(None, max_length=50)
    rounding_fields: ClassVar[set[str]] = {"amount", "interest_rate"}


class Loan(CustomBaseModel):
    id: Optional[str] = Field(None, max_length=50)
    recording_date: Optional[int] = None
    sale_date: Optional[int] = None
    loan_recording_date: Optional[int] = None
    loan_due_date: Optional[int] = None
    loan_term: Optional[int] = None
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    loan_interest_rate: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    estimated_loan_payment: Optional[Decimal] = Field(
        None, max_digits=12, decimal_places=2
    )
    estimated_loan_balance: Optional[Decimal] = Field(
        None, max_digits=12, decimal_places=2
    )
    document_number: Optional[str] = Field(None, max_length=50)
    document_type: Optional[str] = Field(None, max_length=255)
    transaction_type: Optional[str] = Field(None, max_length=255)
    loan_type: Optional[str] = Field(None, max_length=255)
    financing_type: Optional[str] = Field(None, max_length=50)
    buyer_names: Optional[str] = Field(None, max_length=255)
    loan_detail: Optional[str] = Field(None, max_length=255)
    purchase_method: Optional[str] = Field(None, max_length=100)
    lender_name: Optional[str] = Field(None, max_length=255)
    amount_estimated: Optional[bool] = None
    document_image_available: Optional[bool] = None
    rounding_fields: ClassVar[set[str]] = {
        "amount",
        "estimated_loan_payment",
        "estimated_loan_balance",
        "loan_interest_rate",
    }


class Transaction(CustomBaseModel):
    id: Optional[int] = None
    recording_date: Optional[Date] = None
    sale_date: Optional[Date] = None
    loan_recording_date: Optional[Date] = None
    loan_due_date: Optional[Date] = None
    loan_term: Optional[int] = None
    amount: Optional[Decimal] = Field(0, max_digits=12, decimal_places=2)
    loan_interest_rate: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    loan_type: Optional[str] = None
    document_number: Optional[str] = None
    document_type: Optional[str] = None
    transaction_type: Optional[str] = None
    financingType: Optional[str] = None
    buyer_names: Optional[str] = None
    seller_names: Optional[str] = None
    purchase_method: Optional[str] = None
    lender_name: Optional[str] = None
    rounding_fields: ClassVar[set[str]] = {"amount", "loan_interest_rate"}
    date_fields: ClassVar[set[str]] = {
        "recording_date",
        "sale_date",
        "loan_recording_date",
        "loan_due_date",
    }


class Foreclosure(CustomBaseModel):
    id: Optional[int] = None
    type: Optional[str] = Field(None, max_length=10)
    recording_date: Optional[int] = None
    default_date: Optional[int] = None
    original_recording_date: Optional[int] = None
    original_document_date: Optional[int] = None
    listing_date: Optional[int] = None
    document_number: Optional[str] = Field(None, max_length=50)
    recording_book: Optional[str] = Field(None, max_length=50)
    recording_page: Optional[str] = Field(None, max_length=50)
    document_type: Optional[str] = Field(None, max_length=100)
    case_number: Optional[str] = Field(None, max_length=50)
    original_document_number: Optional[str] = Field(None, max_length=50)
    original_recording_book: Optional[str] = Field(None, max_length=50)
    original_recording_page: Optional[str] = Field(None, max_length=50)
    trustee_last_name: Optional[str] = Field(None, max_length=255)
    borrower1_company: Optional[str] = Field(None, max_length=255)
    borrower2_company: Optional[str] = Field(None, max_length=255)
    report_description: Optional[str] = None
    recording_book_page: Optional[str] = Field(None, max_length=255)
    original_recording_book_page: Optional[str] = Field(None, max_length=255)
    borrower1_name: Optional[str] = Field(None, max_length=255)
    borrower2_name: Optional[str] = Field(None, max_length=255)
    borrower_names: Optional[str] = None
    trustee_name: Optional[str] = Field(None, max_length=255)
    type_name: Optional[str] = Field(None, max_length=50)
    active: Optional[bool] = Field(default=False)


class Lien(CustomBaseModel):
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    listing_amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    listing_date: Optional[Date] = None
    recording_date: Optional[Date] = None
    tax_date: Optional[Date] = None
    tax_period_min: Optional[Date] = None
    tax_period_max: Optional[Date] = None
    fips: Optional[str] = Field(None, max_length=10)
    apn_unformatted: Optional[str] = Field(None, max_length=50)
    block: Optional[str] = Field(None, max_length=20)
    range: Optional[str] = Field(None, max_length=20)
    township: Optional[str] = Field(None, max_length=20)
    district: Optional[str] = Field(None, max_length=20)
    district_suffix: Optional[str] = Field(None, max_length=10)
    land_lot: Optional[str] = Field(None, max_length=20)
    lot_number: Optional[str] = Field(None, max_length=10)
    damar_document_code: Optional[str] = Field(None, max_length=10)
    document_type: Optional[str] = Field(None, max_length=50)
    document_number: Optional[str] = Field(None, max_length=20)
    recording_book: Optional[str] = Field(None, max_length=20)
    recording_page: Optional[str] = Field(None, max_length=20)
    tax_type: Optional[str] = Field(None, max_length=50)
    tax_number: Optional[str] = Field(None, max_length=20)
    creditor_name: Optional[str] = Field(None, max_length=100)
    stay_ordered: Optional[bool] = Field(default=False)
    installment_judgment: Optional[bool] = Field(default=False)
    assignee_of_record: Optional[bool] = Field(default=False)
    additional_judgment_debtors: Optional[bool] = Field(default=False)
    judgment_creditor: Optional[bool] = Field(default=False)
    bankruptcy_asset: Optional[bool] = Field(default=False)
    bankruptcy_pro_se: Optional[bool] = Field(default=False)
    type: Optional[str] = Field(None, max_length=1)
    effective_debtor_names: Optional[str] = Field(None, max_length=100)
    effective_petitioner_names: Optional[str] = Field(None, max_length=100)
    debtor_name: Optional[str] = Field(None, max_length=100)
    type_description: Optional[str] = Field(None, max_length=100)
    recording_book_page: Optional[str] = Field(None, max_length=50)
    date_fields: ClassVar[set[str]] = {
        "recording_date",
        "listing_date",
        "loan_recording_date",
        "tax_date",
        "tax_period_min",
        "tax_period_max",
    }


class Property(CustomBaseModel):
    address: str
    is_auction: bool
    is_obit: bool
    source_name: str
    property_type: Optional[str] = None
    occupancy: Optional[str] = None
    auctions: List[Auction] = []
    debts: List[Debt] = []
    sales: List[Sale] = []
    legal_proceedings: List[LegalProceeding] = []

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    def recursive_convert_to_float(self, data):
        if isinstance(data, dict):
            return {
                key: self.recursive_convert_to_float(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self.recursive_convert_to_float(item) for item in data]
        elif isinstance(data, Decimal):
            return float(data)
        return data

    def recursive_filter_null(self, data):
        if isinstance(data, dict):
            filtered = {
                k: v
                for k, v in (
                    (k, self.recursive_filter_null(v)) for k, v in data.items()
                )
                if v is not None
            }
            return filtered or None
        elif isinstance(data, list):
            filtered = [
                item
                for item in (self.recursive_filter_null(item) for item in data)
                if item is not None
            ]
            return filtered or None
        elif isinstance(data, str):
            stripped = data.strip()
            return stripped if stripped else None
        return data

    def model_dump(self, include: set = None, exclude: set = None):
        data = super().model_dump(include=include, exclude=exclude)
        filtered_data = self.recursive_convert_to_float(
            self.recursive_filter_null(data)
        )
        return {"stage": "NEW", "property": filtered_data}
