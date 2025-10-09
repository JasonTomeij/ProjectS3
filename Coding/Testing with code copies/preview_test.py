import pandas as pd


def analyze_csv(filepath, preview_rows=5):
    """
    Analyze and preview a CSV file

    Parameters:
    filepath (str): Path to the CSV file
    preview_rows (int): Number of rows to preview
    """
    try:
        # Read the CSV file
        print(f"Loading CSV file: {filepath}")
        df = pd.read_csv(filepath)

        # Basic information about the dataset
        print("\n=== Dataset Information ===")
        print(f"Number of rows: {len(df):,}")
        print(f"Number of columns: {len(df.columns):,}")

        # Column names and data types
        print("\n=== Columns and Data Types ===")
        for col in df.columns:
            print(f"Column: {col}")
            print(f"Data type: {df[col].dtype}")
            print(f"Non-null count: {df[col].count():,}")
            print("---")

        # Preview of the data
        print(f"\n=== First {preview_rows} rows of data ===")
        print(df.head(preview_rows))

        # Basic statistics
        print("\n=== Numeric Column Statistics ===")
        print(df.describe())

        return df

    except Exception as e:
        print(f"Error analyzing CSV: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def preview_column_values(df, column_name, n_values=5):
    """
    Preview unique values in a specific column
    """
    if df is not None and column_name in df.columns:
        unique_values = df[column_name].unique()
        print(f"\n=== Sample of unique values in column '{column_name}' ===")
        print(f"Total unique values: {len(unique_values):,}")
        print(f"First {n_values} unique values:")
        print(unique_values[:n_values])


if __name__ == "__main__":
    # Your file path
    filepath = "/Users/dennishagen/Desktop/Verzameldocumenten master/dialogic_hu_2017_2021.csv"

    # Analyze the CSV file
    df = analyze_csv(filepath)

    if df is not None:
        # Ask user if they want to preview specific columns
        print("\nWould you like to preview values from specific columns?")
        print("Available columns:")
        for i, col in enumerate(df.columns):
            print(f"{i + 1}. {col}")

        response = input("\nEnter column number to preview (or press Enter to skip): ")
        if response.isdigit() and 1 <= int(response) <= len(df.columns):
            column_name = df.columns[int(response) - 1]
            preview_column_values(df, column_name)