import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type, PhoneNumberType
import argparse
import json
import requests
from datetime import datetime

# Indo prefix mapping (simplified)
prefix_to_city = {
    "62811": "Jakarta",
    "62812": "Medan",
    "62813": "Surabaya",
    "62822": "Bandung",
    "62823": "Yogyakarta",
    "62821": "Semarang",
    "62857": "Makassar",
    "62817": "Palembang"
}

disposable_carriers = ["Hushed", "Burner", "TextNow", "TextFree"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def guess_city(phone_number):
    for prefix, city in prefix_to_city.items():
        if phone_number.startswith(prefix):
            return city
    return "Unknown"

def get_number_type(num_type):
    types = {
        PhoneNumberType.MOBILE: "Mobile",
        PhoneNumberType.FIXED_LINE: "Fixed Line",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed or Mobile",
        PhoneNumberType.TOLL_FREE: "Toll Free",
        PhoneNumberType.PREMIUM_RATE: "Premium Rate",
        PhoneNumberType.VOIP: "VOIP",
        PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
        PhoneNumberType.PAGER: "Pager",
        PhoneNumberType.UAN: "UAN",
        PhoneNumberType.UNKNOWN: "Unknown"
    }
    return types.get(num_type, "Unknown")

def check_whatsapp_presence(phone_number):
    try:
        resp = requests.get(f"https://wa.me/{phone_number}", headers=HEADERS, timeout=5)
        return resp.status_code == 200
    except:
        return False

def check_telegram_presence(phone_number):
    try:
        resp = requests.get(f"https://t.me/+{phone_number[1:]}", headers=HEADERS, timeout=5)
        return resp.status_code == 200
    except:
        return False

def recon_phone_number(phone_number):
    parsed = phonenumbers.parse(phone_number, "ID")
    num_type = number_type(parsed)
    carrier_name = carrier.name_for_number(parsed, 'en')

    wa = check_whatsapp_presence(phone_number)
    tg = check_telegram_presence(phone_number)

    is_disposable = carrier_name in disposable_carriers
    sim_swap_risk = get_number_type(num_type) in ["VOIP", "Personal Number"]

    risk_score = 0
    if is_disposable: risk_score += 2
    if sim_swap_risk: risk_score += 2
    if wa or tg: risk_score += 1
    threat_rating = "High" if risk_score >= 4 else "Moderate" if risk_score >= 2 else "Low"

    result = {
        "input_number": phone_number,
        "valid_number": phonenumbers.is_valid_number(parsed),
        "possible_number": phonenumbers.is_possible_number(parsed),
        "country_code": parsed.country_code,
        "region": geocoder.description_for_number(parsed, 'en'),
        "carrier": carrier_name,
        "number_type": get_number_type(num_type),
        "timezone": list(timezone.time_zones_for_number(parsed)),
        "city_guess": guess_city(phone_number.replace("+", "")),
        "social_presence": {
            "whatsapp": wa,
            "telegram": tg
        },
        "disposable_number": is_disposable,
        "sim_swap_risk": sim_swap_risk,
        "threat_rating": threat_rating,
        "formats": {
            "national": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
            "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "E.164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        }
    }
    return result

def print_result(data):
    print("======== IndoRecon OPSEC + Social Report ========")
    print(f"Number Entered       : {data['input_number']}")
    print(f"Valid Number         : {data['valid_number']}")
    print(f"Possible Number      : {data['possible_number']}")
    print(f"Country Code         : {data['country_code']}")
    print(f"Region / Location    : {data['region']}")
    print(f"Carrier              : {data['carrier']}")
    print(f"Number Type          : {data['number_type']}")
    print(f"City (Prefix Guess)  : {data['city_guess']}")
    print(f"Timezone(s)          : {', '.join(data['timezone'])}")
    print(f"National Format      : {data['formats']['national']}")
    print(f"International Format : {data['formats']['international']}")
    print(f"E.164 Format         : {data['formats']['E.164']}")
    print(f"Disposable Number    : {'Yes' if data['disposable_number'] else 'No'}")
    print(f"SIM Swap Risk        : {'Yes' if data['sim_swap_risk'] else 'No'}")
    print(f"Threat Rating        : {data['threat_rating']}")
    print("-------- Social Media Presence --------")
    print(f"WhatsApp Registered  : {'Yes' if data['social_presence']['whatsapp'] else 'No'}")
    print(f"Telegram Registered  : {'Yes' if data['social_presence']['telegram'] else 'No'}")
    print("=================================================")

def export_to_file(data, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"IndoRecon_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[+] Results saved to: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IndoRecon - Phone Number Recon Tool")
    parser.add_argument("-n", "--number", required=True, help="Phone number to analyze (e.g. +628123456789)")
    parser.add_argument("-s", "--silent", action="store_true", help="Silent mode (no output)")
    parser.add_argument("-e", "--export", nargs="?", const=True, help="Export results to JSON file")

    args = parser.parse_args()

    try:
        result = recon_phone_number(args.number)

        if not args.silent:
            print_result(result)

        if args.export:
            export_to_file(result, args.export if isinstance(args.export, str) else None)

    except Exception as e:
        print(f"[!] Error: {e}")
