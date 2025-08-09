import sys
sys.path.append("/home/ubuntu/financial-data-parser/financial-data-parser/src/core")
from format_parser import FormatParser

parser = FormatParser()

print("--- Amount Parsing Tests ---")
test_amounts = [
    "$1,234.56",
    "(2,500.00)",
    "€1.234,56",
    "1.5M",
    "₹1,23,456",
    "1234.56-",
    "1000K",
    "5.2B",
    "abc",
    None
]

for amount_str in test_amounts:
    parsed_amount = parser.parse_amount(amount_str)
    print(f"  Original: {amount_str}, Parsed: {parsed_amount}")

print("\n--- Date Parsing Tests ---")
test_dates = [
    "12/31/2023",
    "2023-12-31",
    "Q4 2023",
    "Dec-23",
    "44927", # Excel serial
    "March 2024",
    "01/01/2025",
    "2025/01/01",
    "abc",
    None
]

for date_str in test_dates:
    parsed_date = parser.parse_date(date_str)
    print(f"  Original: {date_str}, Parsed: {parsed_date}")


