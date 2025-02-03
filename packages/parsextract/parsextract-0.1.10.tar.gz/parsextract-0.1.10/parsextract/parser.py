import re

from parsextract.constants import ALL_TLDS

IP_REGEX = r"(?i)(?<![a-zA-Z0-9:.])(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])){3}(?![a-zA-Z0-9/.])"
DOMAIN_REGEX = r"""(?i)(?:^|\s|["']|[,])((?:(?:[A-Z0-9_](?:[A-Z0-9_-]{0,61}[A-Z0-9_])?\.)+)(?:[A-Z0-9-]{1,63}(?<!-)))(?!(?:/[^\s/]+))(?![a-zA-Z0-9@])"""
EMAIL_REGEX = r"(?<!@)\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}\b(?!@)"

def extract_ips(text):
    """Extract IP addresses from text."""
    return list(set(re.findall(IP_REGEX, text)))

def extract_domains(text):
    """Extract domains from text and validate their TLDs."""
    matches = re.findall(DOMAIN_REGEX, text)
    valid_domains = set({})
    for domain in matches:
        try:
            tld = f""".{domain.split(".")[-1]}"""
            if tld in ALL_TLDS:
                valid_domains.add(domain)
        except Exception:
            pass
    return list(valid_domains)

def extract_emails(text):
    """Extract email addresses from text."""
    return list(set(re.findall(EMAIL_REGEX, text)))