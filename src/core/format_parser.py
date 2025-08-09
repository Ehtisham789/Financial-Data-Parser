import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
import locale

class FormatParser:
    def __init__(self):
        # Set locale for currency parsing (e.g., for European format)
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except locale.Error:
            print("Warning: Could not set locale to en_US.UTF-8. Some currency parsing might be affected.")

    def parse_amount(self, value, detected_format=None):
        if pd.isna(value):
            return None
        
        s_value = str(value).strip()

        # Handle abbreviated amounts (K, M, B)
        if re.match(r'^[\d.]+[KMB]$', s_value, re.IGNORECASE):
            multiplier = 1
            if s_value.endswith('K') or s_value.endswith('k'):
                multiplier = 1000
            elif s_value.endswith('M') or s_value.endswith('m'):
                multiplier = 1000000
            elif s_value.endswith('B') or s_value.endswith('b'):
                multiplier = 1000000000
            num_part = s_value[:-1]
            try:
                return Decimal(num_part) * multiplier
            except InvalidOperation:
                pass

        # Handle negative in parentheses (e.g., (1,234.56))
        is_negative = False
        if re.match(r'^\([\d,.]+\)$', s_value):
            s_value = s_value[1:-1]
            is_negative = True

        # Handle trailing negative (e.g., 1234.56-)
        if s_value.endswith('-'):
            s_value = s_value[:-1]
            is_negative = True

        # Remove currency symbols and spaces
        s_value = re.sub(r'[^\d.,-]', '', s_value)

        # Indian format: remove all commas, decimal is always a dot
        # This regex checks for the Indian numbering system pattern (e.g., 1,23,456.78)
        # It looks for a digit, then optionally groups of two digits preceded by a comma, then a comma and three digits, then optional decimal part
        if re.match(r'^\d{1,3}(?:,\d{2})*(?:,\d{3})?(?:\.\d+)?$', s_value):
            s_value = s_value.replace(',', '')
        # European format (e.g., 1.234,56) - comma as decimal separator
        elif ',' in s_value and '.' in s_value:
            if s_value.rfind(',') > s_value.rfind('.'): # European style: 1.234,56
                s_value = s_value.replace('.', '').replace(',', '.')
            else: # US style: 1,234.56, remove comma
                s_value = s_value.replace(',', '')
        elif ',' in s_value and s_value.count(',') == 1 and s_value.rfind(',') == len(s_value) - 3: # US style: 1,234
            s_value = s_value.replace(',', '')
        elif ',' in s_value: # Only comma, assume European style if not US thousands
            s_value = s_value.replace(',', '.')

        try:
            amount = Decimal(s_value)
            return -amount if is_negative else amount
        except InvalidOperation:
            return None

    def parse_date(self, value, detected_format=None):
        if pd.isna(value):
            return None

        s_value = str(value).strip()

        # Excel serial date
        if s_value.isdigit() and len(s_value) == 5:
            try:
                # Excel serial date for Windows (1900-based date system)
                return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(s_value) - 2)
            except ValueError:
                pass

        # Quarter format (e.g., Q1 2024, Q1-24)
        if re.match(r'Q[1-4][\s-]?\d{2,4}', s_value, re.IGNORECASE):
            year_match = re.search(r'\d{2,4}', s_value)
            if year_match:
                year = int(year_match.group())
                if len(str(year)) == 2: # Handle 2-digit years
                    year += 2000 if year < 50 else 1900 # Simple heuristic
                quarter = int(s_value[1])
                month = (quarter - 1) * 3 + 1
                return datetime(year, month, 1)

        # Month Year format (e.g., Mar 2024, March 2024)
        if re.match(r'[A-Za-z]{3,9}\s\d{4}', s_value, re.IGNORECASE):
            try:
                return datetime.strptime(s_value, '%b %Y')
            except ValueError:
                try:
                    return datetime.strptime(s_value, '%B %Y')
                except ValueError:
                    pass
        
        # Mon-YY format (e.g., Dec-23)
        if re.match(r'[A-Za-z]{3}-\d{2}', s_value, re.IGNORECASE):
            try:
                return datetime.strptime(s_value, '%b-%y')
            except ValueError:
                pass

        # Standard date formats
        date_formats = [
            '%m/%d/%Y', '%d/%m/%Y',  # MM/DD/YYYY, DD/MM/YYYY
            '%Y-%m-%d', '%d-%b-%Y',  # YYYY-MM-DD, DD-MON-YYYY
            '%Y/%m/%d', '%d/%m/%y', '%m/%d/%y', # Additional common formats
            '%b %d, %Y', '%B %d, %Y' # e.g., Jan 01, 2023
        ]
        for fmt in date_formats:
            try:
                return datetime.strptime(s_value, fmt)
            except ValueError:
                pass

        return None

    def normalize_currency(self, value):
        # This method would be more complex in a real scenario, involving currency conversion rates.
        # For this project, we'll assume normalization means converting to a standard Decimal format.
        return self.parse_amount(value)

    def handle_special_formats(self, value):
        # This method can be extended for other special formats not covered by parse_amount or parse_date
        return value

import pandas as pd


