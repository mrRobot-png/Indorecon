# Indorecon
Indonesian Phone Number Scanner 
IndoRecon — Phone Number Recon Tool

IndoRecon is an OSINT-powered phone number reconnaissance script, designed to give you deep insights into Indonesian (+62) phone numbers, blending geolocation, carrier info, OPSEC checks, and social media presence detection.


---

Features

Detect valid and possible numbers.

Identify carrier and number type.

Guess Indonesian city based on prefix.

Detect WhatsApp and Telegram registration.

Flag disposable numbers.

Assess SIM swap risk.

Assign an overall threat rating.

Export results to JSON for reporting.



---

Usage

Run IndoRecon directly from your terminal:

python indo_recon.py -n "+628123456789"

Options:


---

Sample Output

======== IndoRecon OPSEC + Social Report ========
Number Entered       : +628123456789
Valid Number         : True
Possible Number      : True
Country Code         : 62
Region / Location    : Indonesia
Carrier              : Telkomsel
Number Type          : Mobile
City (Prefix Guess)  : Jakarta
Timezone(s)          : Asia/Jakarta
National Format      : 0812-3456-789
International Format : +62 812-3456-789
E.164 Format         : +628123456789
Disposable Number    : No
SIM Swap Risk        : No
Threat Rating        : Low
-------- Social Media Presence --------
WhatsApp Registered  : Yes
Telegram Registered  : No
=================================================


---

Requirements

Python 3.x

phonenumbers

requests


Install dependencies:

pip install phonenumbers requests


---

Disclaimer

> IndoRecon is intended for educational and ethical use only.
Always obtain permission before scanning phone numbers that aren’t yours.

