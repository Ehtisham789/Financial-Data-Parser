import pandas as pd
import numpy as np
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

class DataTypeDetector:
    def __init__(self):
        self.date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY or DD/MM/YYYY
            r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
            r'\d{1,2}-[A-Za-z]{3}-\d{4}',  # DD-MON-YYYY
            r'Q[1-4][\s-]?\d{4}',  # Q1 2024, Q1-24
            r'[A-Za-z]{3,9}\s\d{4}',  # Mar 2024, March 2024
            r'^\d{5}$'  # Excel serial dates (5 digits)
        ]
        
        self.currency_patterns = [
            r'^\$[\d,]+\.?\d*$',  # $1,234.56
            r'^€[\d.,]+$',  # €1.234,56
            r'^₹[\d,]+\.?\d*$',  # ₹1,23,456.78
            r'^\([\d,]+\.?\d*\)$',  # (1,234.56) negative
            r'^[\d,]+\.?\d*-$',  # 1234.56- trailing negative
            r'^[\d.]+[KMB]$'  # 1.23K, 2.5M, 1.2B
        ]

    def detect_column_type(self, column_data):
        # Remove null values for analysis
        clean_data = column_data.dropna()
        
        if len(clean_data) == 0:
            return {'type': 'string', 'confidence': 0.0, 'format': None}
        
        # Convert to string for pattern matching
        str_data = clean_data.astype(str)
        
        # Try parsing as dates first
        date_score = self._detect_date_format(str_data)
        
        # Try parsing as numbers (handle currency symbols)
        number_score = self._detect_number_format(str_data)
        
        # Default to string if neither works
        string_score = self._classify_string_type(str_data)
        
        # Return the type with highest confidence
        scores = {
            'date': date_score,
            'number': number_score,
            'string': string_score
        }
        
        best_type = max(scores, key=lambda k: scores[k]['confidence'])
        return scores[best_type]

    def _detect_date_format(self, sample_values):
        date_matches = 0
        detected_format = None
        
        for value in sample_values[:100]:  # Sample first 100 values
            for pattern in self.date_patterns:
                if re.match(pattern, str(value)):
                    date_matches += 1
                    detected_format = pattern
                    break
            
            # Try pandas date parsing
            try:
                pd.to_datetime(value)
                date_matches += 1
            except:
                pass
        
        confidence = date_matches / min(len(sample_values), 100)
        return {
            'type': 'date',
            'confidence': confidence,
            'format': detected_format
        }

    def _detect_number_format(self, sample_values):
        number_matches = 0
        detected_format = None
        
        for value in sample_values[:100]:  # Sample first 100 values
            # Check currency patterns
            for pattern in self.currency_patterns:
                if re.match(pattern, str(value)):
                    number_matches += 1
                    detected_format = pattern
                    break
            
            # Try direct numeric conversion
            try:
                # Remove common currency symbols and formatting
                clean_value = re.sub(r'[$€₹,()]', '', str(value))
                clean_value = clean_value.replace('-', '')
                float(clean_value)
                number_matches += 1
            except ValueError:
                pass
        
        confidence = number_matches / min(len(sample_values), 100)
        return {
            'type': 'number',
            'confidence': confidence,
            'format': detected_format
        }

    def _classify_string_type(self, sample_values):
        # Analyze string patterns to classify type
        string_types = {
            'account_name': 0,
            'description': 0,
            'reference': 0,
            'category': 0,
            'general': 0
        }
        
        for value in sample_values[:50]:  # Sample first 50 values
            value_str = str(value).lower()
            
            # Account name patterns
            if any(keyword in value_str for keyword in ['account', 'cash', 'bank', 'receivable', 'payable']):
                string_types['account_name'] += 1
            # Description patterns
            elif len(value_str) > 20 and any(keyword in value_str for keyword in ['payment', 'invoice', 'transaction']):
                string_types['description'] += 1
            # Reference patterns
            elif re.match(r'^[A-Z0-9-]+$', str(value)) and len(str(value)) < 20:
                string_types['reference'] += 1
            # Category patterns
            elif len(value_str) < 30 and not re.search(r'\d', value_str):
                string_types['category'] += 1
            else:
                string_types['general'] += 1
        
        best_string_type = max(string_types, key=string_types.get)
        confidence = 0.8  # Default confidence for string classification
        
        return {
            'type': 'string',
            'confidence': confidence,
            'format': best_string_type
        }

    def analyze_column(self, data):
        """Main method to analyze a column and return its detected type"""
        return self.detect_column_type(data)

