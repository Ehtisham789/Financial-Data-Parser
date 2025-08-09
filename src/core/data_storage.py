import pandas as pd

class DataStorage:
    def __init__(self):
        self.data_frames = {}
        self.indexes = {}
        self.metadata = {}

    def store_data(self, name, dataframe, metadata=None):
        self.data_frames[name] = dataframe
        self.metadata[name] = metadata if metadata is not None else {}
        print(f"Stored data for {name}. Shape: {dataframe.shape}")

    def create_indexes(self, name, columns):
        if name not in self.data_frames:
            print(f"Error: Dataset {name} not found.")
            return
        
        df = self.data_frames[name]
        self.indexes[name] = {}
        for col in columns:
            if col in df.columns:
                # For simplicity, we'll just store the column itself as an 'index'
                # In a real system, this would involve more complex indexing structures (e.g., B-trees, hash maps)
                self.indexes[name][col] = df[col]
                print(f"Created index for column '{col}' in dataset '{name}'")
            else:
                print(f"Warning: Column '{col}' not found in dataset '{name}'")

    def query_by_criteria(self, name, filters=None):
        if name not in self.data_frames:
            print(f"Error: Dataset {name} not found.")
            return pd.DataFrame()

        df = self.data_frames[name]
        if filters is None:
            return df

        filtered_df = df.copy()
        for column, value in filters.items():
            if column in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[column] == value]
            else:
                print(f"Warning: Filter column '{column}' not found in dataset '{name}'")
        return filtered_df

    def aggregate_data(self, name, group_by, measures, agg_func='sum'):
        if name not in self.data_frames:
            print(f"Error: Dataset {name} not found.")
            return pd.DataFrame()

        df = self.data_frames[name]
        if not all(col in df.columns for col in group_by):
            print(f"Error: One or more group_by columns not found in dataset '{name}'")
            return pd.DataFrame()
        if not all(col in df.columns for col in measures):
            print(f"Error: One or more measure columns not found in dataset '{name}'")
            return pd.DataFrame()

        try:
            return df.groupby(group_by)[measures].agg(agg_func)
        except Exception as e:
            print(f"Error during aggregation: {e}")
            return pd.DataFrame()

    def get_data(self, name):
        return self.data_frames.get(name)

    def get_metadata(self, name):
        return self.metadata.get(name)

