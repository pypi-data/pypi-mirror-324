import usaddress
import re
from datetime import datetime
from geopy.distance import geodesic


def get_phones_info(phones):
    if not phones:
        return []

    extracted_info = []
    for phone in phones:
        extracted_info.append(
            {
                "phone_number": phone.get("phoneNumber"),
                "phone_type": phone.get("phoneType"),
                "is_connected": phone.get("isConnected"),
            }
        )
    return extracted_info


def get_emails_info(emails):
    if not emails:
        return []

    extracted_info = []
    for email in emails:
        extracted_info.append(
            {
                "email_address": email.get("emailAddress"),
            }
        )
    return extracted_info


def extract_address_info(address):
    return {
        "address_line": address.get("fullAddress"),
        "city": address.get("city"),
        "state": address.get("state"),
        "zip_code": address.get("zip"),
        "latitude": address.get("latitude"),
        "longitude": address.get("longitude"),
    }


def get_addresses_info(addresses, person_type, latitude, longitude):
    if not addresses:
        return []

    processed_coordinates = set()
    extracted_info = []

    for address in addresses:
        addr_latitude = address.get("latitude")
        addr_longitude = address.get("longitude")

        if (addr_latitude, addr_longitude) in processed_coordinates:
            continue

        processed_coordinates.add((addr_latitude, addr_longitude))

        if person_type in ["Neighbor", "Owner"]:
            if is_property_too_close(
                latitude, longitude, addr_latitude, addr_longitude, 150
            ):
                extracted_info.append(extract_address_info(address))
        else:
            extracted_info.append(extract_address_info(address))

    return extracted_info


def camel_to_snake(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def fix_date_fields(date_input):
    if isinstance(date_input, datetime):
        return date_input.strftime("%Y-%m-%d")

    if isinstance(date_input, (int, float)):
        try:
            return datetime.fromtimestamp(date_input/1000).strftime("%Y-%m-%d")
        except (ValueError, OSError):
            return None

    if isinstance(date_input, str):
        date_formats = [
            "%A, %b %d, %Y",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y/%m/%d",
            "%b %d, %Y",
            "%B %d, %Y",
            "%d %b %Y",
            "%d %B %Y",
            "%Y.%m.%d",
            "%d.%m.%Y",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d-%m-%Y %H:%M:%S",
            "%m-%d-%Y %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
        ]
        for fmt in date_formats:
            try:
                return datetime.strptime(date_input, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue

    return None


def check_address(address):
    try:
        parsed_address = usaddress.tag(address)[0]
        check = all(
            [
                parsed_address.get("AddressNumber", None),
                parsed_address.get("StreetName", None),
                parsed_address.get("StateName", None),
                parsed_address.get("ZipCode", None),
            ]
        )
        return check
    except Exception as e:
        raise(e)


def reformat_address(address):
    try:
        parsed_address = usaddress.tag(address)[0]

        address_number = parsed_address.get("AddressNumber", "").strip()
        street_name = parsed_address.get("StreetName", "").strip()
        street_name_post_type = parsed_address.get("StreetNamePostType", "").strip()
        state_name = parsed_address.get("StateName", "").strip()
        zip_code = parsed_address.get("ZipCode", "").strip()

        occupancy_identifier = parsed_address.get("OccupancyIdentifier", "").strip()
        if occupancy_identifier:
            occupancy_identifier = (
                occupancy_identifier
                if occupancy_identifier.startswith("#")
                else f"#{occupancy_identifier}"
            )
        else:
            street_name_post_type += ","

        formatted_address = " ".join(
            filter(
                None,
                [
                    address_number,
                    street_name,
                    street_name_post_type,
                    occupancy_identifier,
                    state_name,
                    zip_code,
                ],
            )
        )

        return ", ".join(part.strip() for part in formatted_address.split(","))

    except Exception:
        return None


def convert_camel_to_snake(obj):
    if isinstance(obj, list):
        return [convert_camel_to_snake(item) for item in obj]
    elif isinstance(obj, dict):
        return {
            camel_to_snake(key): convert_camel_to_snake(value)
            for key, value in obj.items()
        }
    else:
        return obj


def is_property_too_close(
    target_lat, target_lon, property_lat, property_lon, max_distance_m
):
    target = (target_lat, target_lon)
    property = (property_lat, property_lon)
    distance = geodesic(target, property).m
    if distance > max_distance_m:
        return False
    return True
