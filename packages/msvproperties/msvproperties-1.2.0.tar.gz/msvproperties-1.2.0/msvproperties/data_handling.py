from .data_models import Debt, Sale, LegalProceeding, Auction, Property
from typing import Optional, Union
from .config import get_config
from .logger import ProcessLogger
from .utils import check_address


def Data(
    session: object,
    address: str,
    is_auction: bool,
    is_obit: bool,
    source_name: str,
    property_type: Optional[str] = None,
    occupancy: Optional[str] = None,
    auction_amount: Optional[Union[float, int]] = None,
    auction_date: Optional[str] = None,
    opening_bid: Optional[Union[float, int]] = None,
    link: Optional[str] = None,
    trustee_sale_number: Optional[str] = None,
    sold_date: Optional[str] = None,
    sold_value: Optional[Union[float, int]] = None,
    sale_status: Optional[str] = None,
    nos_amount: Optional[Union[float, int]] = None,
    max_debt: Optional[Union[float, int]] = None,
    trustee_name: Optional[str] = None,
    trustee_phone: Optional[str] = None,
    final_judgment: Optional[Union[float, int]] = None,
    plaintiff: Optional[str] = None,
    attorney_name: Optional[str] = None,
    attorney_phone: Optional[str] = None,
    attorney_bar_no: Optional[str] = None,
    attorney_firm: Optional[str] = None,
    defendants: Optional[str] = None,
    total_amount_owed: Optional[Union[float, int]] = None,
    document_name: Optional[str] = None,
    case_number: Optional[str] = None,
    case_type: Optional[str] = None,
    date_of_filing: Optional[str] = None,
    probate_case_number: Optional[str] = None,
) -> dict:
    """
    Initialize an AuctionProperty instance with the following attributes:

    address: address of the property.
    is_auction: Boolean indicating if the property is an auction property.
    is_obit: Boolean indicating if the lead is an obit or not.
    source_name: Name of the source where the property information is obtained.
    opening_bid: Opening bid amount for the auction.
    max_debt: maximum amount of debt.
    auction_value: highest bid at the auction.
    auction_date: Date of the auction.
    property_type: Type of the property (e.g., residential, commercial).
    link: Link to the property listing or auction details.
    occupancy: Occupancy status of the property.
    trustee_name: Name of the trustee handling the auction.
    trustee_phone: Phone number of the trustee.
    trustee_sale_number: Sale number associated with the trustee.
    sold_date: Date the property was sold.
    sold_value: Value for which the property was sold.
    final_judgment: Final judgment amount.
    plaintiff: Plaintiff in the case associated with the property.
    attorney_name: Name of the attorney handling the case.
    attorney_phone: Phone number of the attorney.
    attorney_bar_no: Bar number of the attorney.
    attorney_firm: Firm the attorney is associated with.
    defendants: Defendants in the case associated with the property.
    sale_status: Sale status of the property.
    nos_amount: Notice of Sale (NOS) amount.
    total_amount_owed: Total amount owed on the property.
    document_name: Name of the document related to the property.
    case_number: Case number associated with the property.
    case_type: Type of the case (e.g., foreclosure, probate).
    date_of_filing: Date the case was filed.
    probate_case_number: Probate case number (if applicable).
    """
    try:
        check_address(address)

        auction = Auction(
            amount=auction_amount,
            date=auction_date,
            opening_bid=opening_bid,
            link=link,
        )

        sale = Sale(
            sale_date=sold_date,
            sale_amount=sold_value,
            sale_status=sale_status,
            nos_amount=nos_amount,
        )

        debt = Debt(amount=max_debt)

        legal_proceeding = LegalProceeding(
            trustee_name=trustee_name,
            trustee_phone=trustee_phone,
            trustee_sale_number=trustee_sale_number,
            final_judgment=final_judgment,
            plaintiff=plaintiff,
            attorney_name=attorney_name,
            attorney_phone=attorney_phone,
            attorney_bar_no=attorney_bar_no,
            attorney_firm=attorney_firm,
            defendants=defendants,
            total_amount_owed=total_amount_owed,
            document_name=document_name,
            case_number=case_number,
            case_type=case_type,
            date_of_filing=date_of_filing,
            probate_case_number=probate_case_number,
        )

        return Property(
            address=address,
            is_auction=is_auction,
            is_obit=is_obit,
            source_name=source_name,
            property_type=property_type,
            occupancy=occupancy,
            auctions=[auction],
            sales=[sale],
            debts=[debt],
            legal_proceedings=[legal_proceeding],
        )
    except Exception as e:
        LOG_PATH, _, _, _ = get_config()
        logger = ProcessLogger(LOG_PATH)
        logger.log_failure(
            address=None,
            cause=e,
            source_name=None,
            is_auction=None,
            user=session.username,
        )
        raise (e)