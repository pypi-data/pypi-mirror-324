import unittest
from parsextract.parser import extract_ips, extract_domains, extract_emails

class TestParseExtract(unittest.TestCase):
    def test_extract_ips(self):
        text = "Valid IP: 192.168.1.1, Invalid IP: 999.999.999.999"
        self.assertEqual(extract_ips(text), ["192.168.1.1"])

    def test_extract_domains(self):
        text = "Website: example.com, another: test.site"
        self.assertEqual(extract_domains(text), ["example.com", "test.site"])

    def test_extract_emails(self):
        text = "Contact: user@example.com, invalid@: noemail.com"
        self.assertEqual(extract_emails(text), ["user@example.com"])

if __name__ == "__main__":
    unittest.main()