import sys
sys.path.append("/home/ubuntu/financial-data-parser/financial-data-parser/src/core")
from excel_processor import ExcelProcessor

file_paths = [
    "/home/ubuntu/financial-data-parser/financial-data-parser/data/sample/KH_Bank.XLSX",
    "/home/ubuntu/financial-data-parser/financial-data-parser/data/sample/Customer_Ledger_Entries_FULL.xlsx"
]

processor = ExcelProcessor()
processor.load_files(file_paths)

sheet_info = processor.get_sheet_info()
print("\n--- Sheet Information ---")
for file_path, info in sheet_info.items():
    print(f"File: {file_path}")
    for sheet_name, details in info["sheets"].items():
        print(f"  Sheet: {sheet_name}")
        print(f"    Dimensions: {details['dimensions']}")
        print(f"    Column Names: {details['column_names']}")

print("\n--- Data Previews ---")
for file_path in file_paths:
    for sheet_name in processor.files[file_path]["sheets"].keys():
        processor.preview_data(file_path, sheet_name, rows=5)


