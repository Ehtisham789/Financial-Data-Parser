import sys
sys.path.append("/home/ubuntu/financial-data-parser/financial-data-parser/src/core")
from data_storage import DataStorage
import pandas as pd

storage = DataStorage()

# Create a sample DataFrame
sample_data = {
    'Date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-03']),
    'Category': ['Rent', 'Salary', 'Utilities', 'Rent'],
    'Amount': [1000, 3000, 150, 1000],
    'Currency': ['USD', 'USD', 'USD', 'USD']
}
sample_df = pd.DataFrame(sample_data)

print("--- Storing Data ---")
storage.store_data('transactions', sample_df, {'description': 'Sample financial transactions'})

print("\n--- Creating Indexes ---")
storage.create_indexes('transactions', ['Date', 'Category'])

print("\n--- Querying Data ---")
query_result = storage.query_by_criteria('transactions', {'Category': 'Rent'})
print("Query for Category=\'Rent\':")
print(query_result)

print("\n--- Aggregating Data ---")
aggregation_result = storage.aggregate_data('transactions', group_by=['Category'], measures=['Amount'])
print("Aggregation by Category (sum of Amount):")
print(aggregation_result)

print("\n--- Retrieving Data ---")
retrieved_df = storage.get_data('transactions')
print("Retrieved full 'transactions' DataFrame:")
print(retrieved_df.head())

print("\n--- Retrieving Metadata ---")
retrieved_metadata = storage.get_metadata('transactions')
print("Retrieved 'transactions' metadata:")
print(retrieved_metadata)


