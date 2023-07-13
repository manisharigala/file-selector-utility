
import re

#Define a list of PII keywords to check against
pii_keywords = ['name', 'phone', 'email', 'address', 'ssn', 'social security']

def check_for_pii(value):
    # Check for PII patterns in the value
    for pattern in pii_keywords:
        if pattern in value.lower():
            return True

    # Check for email addresses
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(email_regex, value):
        return True

    # Check for phone numbers
    phone_regex = r'\b(?:\+?1[-.\s]?)?(?:\(?([2-9][0-8][0-9])\)?[-.\s]?)(?:([2-9][0-9]{2})[-.\s]?)(?:([0-9]{4})(?:[-.\s]?([0-9]{1,4}))?)\b'
    if re.search(phone_regex, value):
        return True

    # Check for home addresses
    address_regex = r'\d+\s+([A-Za-z]+|[A-Za-z]+\s[A-Za-z]+)\s+([A-Za-z]+|[A-Za-z]+\s[A-Za-z]+)'
    if re.search(address_regex, value):
        return True
    
    # Check for SSN
    ssn_regex = r'\b\d{3}[-]?\d{2}[-]?\d{4}\b'
    if re.search(ssn_regex, value):
        return True
    
    # Check for credit card numbers
    cc_regex = r'\b(?:\d[ -]*?){13,16}\b'
    if re.search(cc_regex, value):
        return True
    
    # Check for dates
    date_regex = r'\b(?:0?[1-9]|1[0-2])[\/-](?:0?[1-9]|[12][0-9]|3[01])[\/-](?:[0-9]{2})?[0-9]{2}\b'
    if re.search(date_regex, value):
        return True
    
    # Check for medical record numbers
    mrn_regex = r'\b\d{7,8}\b'
    if re.search(mrn_regex, value):
        return True
    
    # Check for driver's license numbers
    dl_regex = r'\b[A-Za-z]{1,2}[ -]?\d{5,6}[ -]?\d{2,5}\b'
    if re.search(dl_regex, value):
        return True
    
    # Check for passport numbers
    passport_regex = r'\b[A-Z]{1,2}[0-9]{6,9}\b'
    if re.search(passport_regex, value):
        return True
    
    # Check for vehicle identification numbers
    vin_regex = r'\b[A-Z0-9]{17}\b'
    if re.search(vin_regex, value):
        return True
    
    # Check for IP addresses
    ip_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    if re.search(ip_regex, value):
        return True
    
    # Check for Biometric identifiers, including finger and voice prints
    biometric_regex = r'\b\d{9}\b'
    if re.search(biometric_regex, value):
        return True
    
    return False