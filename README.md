# Financial Data Parser

## Project Overview

This project implements a robust financial data parsing system designed to process Excel files, intelligently detect data types, handle various formats, and store data in optimized structures for fast retrieval and analysis. It addresses common challenges in financial data management, such as inconsistent formatting and diverse data representations.

## Features

- **Basic Excel Processing (Phase 1)**:
  - Reads Excel files (`.xlsx`, `.xls`) using both `pandas` and `openpyxl`.
  - Handles multiple worksheets within each Excel file.
  - Displays basic file information, including sheet names, dimensions (rows and columns), and column headers.
  - Provides data preview functionality for quick inspection of sheet contents.

- **Data Type Detection (Phase 2)**:
  - Implements intelligent column classification to identify data as string, number, or date types.
  - Detects specific date formats (e.g., MM/DD/YYYY, YYYY-MM-DD, Quarter formats, Excel serial dates).
  - Detects various number formats, including currency symbols ($, €, ₹), parenthetical negatives, trailing negatives, and abbreviated amounts (K, M, B).
  - Assigns a confidence score to each detected data type.

- **Format Parsing Challenges (Phase 3)**:
    - Robustly parses diverse financial amount formats into standardized decimal values, handling:
      - Currency symbols and thousands separators from different locales (e.g., US, European, Indian).
      - Negative numbers represented in parentheses or with trailing negatives.
      - Abbreviated amounts (e.g., "1.5M" for 1,500,000).
  - Converts various date string formats into standard `datetime` objects.

- **Data Structure Implementation (Phase 4)**:
  - Utilizes `pandas.DataFrame` for efficient in-memory data storage.
  - Supports conceptual indexing for fast lookups by multiple criteria.
  - Enables powerful querying capabilities to filter data based on specific conditions.
  - Provides aggregation functionalities (e.g., sum, average) for financial measures, grouped by specified criteria.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:

1. **Install dependencies**:
The project relies on `pandas` and `openpyxl`. You can install them using pip:

## Project Structure

```
financial-data-parser/
├── config/
│   └── settings.py
├── data/
│   ├── processed/
│   └── sample/
│       ├── Customer_Ledger_Entries_FULL.xlsx
│       └── KH_Bank.XLSX
├── examples/
│   ├── advanced_parsing.py
│   ├── basic_usage.py
│   ├── performance_demo.py
│   ├── phase1_test.py
│   ├── phase2_test.py
│   ├── phase3_test.py
│   └── phase4_test.py
├── scripts/
│   └── run_benchmarks.py
├── src/
│   ├── core/
│   │   ├── data_storage.py
│   │   ├── excel_processor.py
│   │   ├── format_parser.py
│   │   └── type_detector.py
│   └── utils/
│       ├── helpers.py
│       └── validators.py
├── tests/
│   ├── test_data_storage.py
│   ├── test_excel_processor.py
│   ├── test_format_parser.py
│   └── test_type_detector.py
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py
```

- `config/`: Configuration files for the project.

- `data/`: Contains sample Excel files (`sample/`) and a directory for processed data (`processed/`).

- `examples/`: Demonstrative scripts showcasing the usage of different modules and testing each phase of the project.

- `scripts/`: Utility scripts for running benchmarks or other operations.

- `src/`: Core source code of the financial data parser.
  - `core/`: Contains the main classes: `ExcelProcessor`, `DataTypeDetector`, `FormatParser`, and `DataStorage`.
  - `utils/`: Helper functions and validation utilities.

- `tests/`: Unit tests for the core modules.

## Usage Examples

To see the functionality in action, you can run the test scripts located in the `examples/` directory:

- **Phase 1 (Basic Excel Processing)**:

- **Phase 2 (Data Type Detection)**:

- **Phase 3 (Format Parsing Challenges)**:

- **Phase 4 (Data Structure Implementation)**:

Each script will print its output to the console, demonstrating the respective phase's capabilities.

## License

This project is licensed under the MIT License - see the LICENSE file for details. *(Note: A **`LICENSE`** file should be created in the root directory of the project with the MIT License text.)*

