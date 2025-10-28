import pandas as pd


def filter_marketing_positions(input_filepath, output_filepath):
    """
    Filter positions to keep only marketing-related roles using positiontitle
    """
    try:
        print("Loading dataset...")
        df = pd.read_csv(input_filepath)

        # Original size
        original_size = len(df)
        print(f"\nOriginal dataset size: {original_size:,} rows")

        # Convert to lowercase for case-insensitive matching
        print("\nFiltering marketing positions...")
        marketing_mask = df['positiontitle'].str.lower().str.contains('marketing', na=False)
        filtered_df = df[marketing_mask]

        # Get statistics
        filtered_size = len(filtered_df)
        print(f"\nFiltered dataset size: {filtered_size:,} rows")
        print(f"Removed {original_size - filtered_size:,} rows")

        # Show distribution of position titles
        print("\nSample of marketing position titles found (top 20):")
        title_counts = filtered_df['positiontitle'].value_counts()
        for title, count in title_counts.head(20).items():
            print(f"- {title}: {count:,} positions")

        # Show distribution by generalized titles
        print("\nDistribution by generalized titles (top 20):")
        gen_title_counts = filtered_df['positiontitlegeneralized'].value_counts()
        for title, count in gen_title_counts.head(20).items():
            print(f"- {title}: {count:,} positions")

        # Save filtered dataset
        print(f"\nSaving filtered dataset to {output_filepath}")
        filtered_df.to_csv(output_filepath, index=False)

        # Show sample of filtered data
        print("\nSample of filtered data (first 5 rows):")
        sample_columns = ['positiontitle', 'positiontitlegeneralized', 'organizationname', 'startingdate']
        print(filtered_df[sample_columns].head())

        return filtered_df

    except Exception as e:
        print(f"Error during filtering: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def analyze_marketing_positions(df):
    """
    Analyze the marketing positions in more detail
    """
    if df is not None and not df.empty:
        print("\n=== Marketing Positions Analysis ===")

        # Analyze starting dates
        if 'startingdate' in df.columns:
            print("\nDate distribution of positions:")
            df['startingdate'] = pd.to_datetime(df['startingdate'], errors='coerce')
            year_counts = df['startingdate'].dt.year.value_counts().sort_index()
            for year, count in year_counts.items():
                if not pd.isna(year):  # Check if year is not NaN
                    print(f"Year {int(year)}: {count:,} positions")

        # Analyze education requirements
        if 'educationdegree' in df.columns:
            print("\nEducation requirements distribution:")
            edu_counts = df['educationdegree'].value_counts()
            for edu, count in edu_counts.items():
                if pd.notna(edu):  # Check if education is not NaN
                    print(f"{edu}: {count:,} positions")

        # Analyze contract types
        if 'typeofcontract' in df.columns:
            print("\nContract type distribution:")
            contract_counts = df['typeofcontract'].value_counts()
            for contract, count in contract_counts.items():
                if pd.notna(contract):  # Check if contract type is not NaN
                    print(f"{contract}: {count:,} positions")

        # Analyze organization types
        print("\nTop 20 organizations posting marketing positions:")
        org_counts = df['organizationname'].value_counts()
        for org, count in org_counts.head(20).items():
            print(f"{org}: {count:,} positions")

        # Analyze geographical distribution
        if 'physicallocationprovince' in df.columns:
            print("\nGeographical distribution:")
            location_counts = df['physicallocationprovince'].value_counts()
            for location, count in location_counts.items():
                if pd.notna(location):  # Check if location is not NaN
                    print(f"{location}: {count:,} positions")


if __name__ == "__main__":
    # File paths
    input_file = "/Users/dennishagen/Desktop/Verzameldocumenten master/dialogic_hu_2017_2021.csv"
    output_file = "/Users/dennishagen/Desktop/Verzameldocumenten master/marketing_positions_2017_2021.csv"

    # Filter the data
    filtered_df = filter_marketing_positions(input_file, output_file)

    # Analyze the filtered data
    if filtered_df is not None:
        analyze_marketing_positions(filtered_df)