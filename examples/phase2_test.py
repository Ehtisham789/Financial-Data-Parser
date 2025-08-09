import sys
sys.path.append("/home/ubuntu/financial-data-parser/financial-data-parser/src/core")
from excel_processor import ExcelProcessor
from type_detector import DataTypeDetector

file_paths = [
    "/home/ubuntu/financial-data-parser/financial-data-parser/data/sample/KH_Bank.XLSX",
    "/home/ubuntu/financial-data-parser/financial-data-parser/data/sample/Customer_Ledger_Entries_FULL.xlsx"
]

processor = ExcelProcessor()
processor.load_files(file_paths)

detector = DataTypeDetector()

print("\n--- Data Type Detection ---")
for file_path in file_paths:
    print(f"\nAnalyzing file: {file_path}")
    for sheet_name in processor.files[file_path]["sheets"].keys():
        df = processor.extract_data(file_path, sheet_name)
        if df is not None:
            print(f"  Sheet: {sheet_name}")
            for column in df.columns:
                if not df[column].empty:
                    detection_result = detector.detect_column_type(df[column])
                    print(f"    Column \'{column}\': Type={detection_result['type']}, Confidence={detection_result['confidence']:.2f}, Format={detection_result['format']}")
                else:
                    print(f"    Column \'{column}\': Empty column, cannot detect type.")


