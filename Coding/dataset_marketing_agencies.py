import pandas as pd

# Define the agencies by category
DIGITAL_AGENCIES = {
    'full_service_digital': [
        'ClickValue', 'Online Dialogue', 'MeasureWorks', 'OrangeValley', 'Adwise',
        'We are you', 'INFO', 'The Valley', 'Macaw', 'Edenspiekermann',
        'Accenture Interactive', 'Conclusion Digital', 'Osudio', 'Merkle Nederland',
        'Fabrique', 'ISAAC', 'TRIMM', 'Xebia', 'Valtech', 'Clockwork', 'Incentro',
        'Mirabeau', 'Emakina', 'Dept', 'Deloitte Digital', 'Youwe', 'E-sites',
        'WeAreBrain', 'ID Factory', 'Bitfactory', 'Arlanet', 'One Shoe',
        'theFactor.e', 'Clever Strategy', 'Bratpack', 'a&m impact', '4net Interactive',
        'Redkiwi', 'Kaliber', 'Netvlies', 'freshheads', 'Burst', 'Jungle Minds',
        'Grrr', 'Snakeware', 'Label A', 'AlienTrick', 'Limesquare', 'Greenberry',
        'Finalist', 'Digitas', 'BLIS Digital', 'TRES', 'Magneds', 'Gracious',
        'WebNL', 'Lukkien', 'DotControl', 'IN10', 'iWink', 'Hoppinger',
        'Elevate Digital', '050media', 'PUURPXL', 'Webton', 'Elephant', 'Axendo',
        'Goeiezaak.com', 'Digital Natives', 'Cube', 'Maatwerk Online', '/CMCG',
        'Zicht Online', 'Scherp Online', 'Pünktlich', 'Chunk Creative Agency',
        'Havana Harbor', 'Energize', 'Isobar', 'ZIGT', 'ACHTUNG!', 'Born05',
        'CODE D\'AZUR', 'DDB Unlimited', 'Havas Lemz', 'RLVNT', 'Viduate',
        'CLEVER°FRANKE', 'Bikkelhart', 'Conversed', 'Concept7', 'Hike One',
        'Valsplat', 'Entopic'
    ],
    'seo_sea_agencies': [
        'Searchresult', 'Yonego', 'SDIM', 'Yourzine', 'Storm Digital', 'Reprise',
        'Netprofiler', 'Artefact', 'Happy Idiots', 'DTG', 'Traffic Builders',
        'iClicks', 'OrangeValley', 'Dept', 'iProspect', 'Maxlead', 'Greenhouse Group'
    ],
    'performance_marketing': [
        'Gradient', 'Harvest Digital', 'Pink Marketing', 'Booming', 'Orangedotcom',
        'Fingerspitz', 'Fosby', 'MvH Media', 'Happy Cactus', 'Traffic Today',
        'Happy Leads', 'Make Marketing Magic', 'PauwR', 'daar-om.nl', 'Nochii',
        'Brandfirm', 'AdResults', 'Tomorrowmen', 'Blauwe Monsters'
    ],
    'lead_generation': [
        'Leadscope', 'Olifant Media', 'Semwerkt', 'RED Online Marketing',
        'DEA.Amsterdam', 'Crowdmedia', 'Bambuu', 'Increase', 'BlooSEM',
        'Hide and Seek', 'Leadrs', 'Conversive', 'DBOM', 'Best4u Internet Marketing'
    ],
    'ai_agencies': [
        'Aidence', 'Dashmote', 'Effect.AI', 'Building Blocks'
    ],
    'email_marketing': [
        'Ematters', 'Yourzine', 'Measuremail', '100%EMAIL', 'e-Village'
    ],
    'ecommerce': [
        'Bluebird Day', 'Evoworks', 'XSARUS', 'Wunderman Thompson Commerce',
        'Experius', 'We Provide', 'ShopWorks', 'Evident', 'Yellowgrape', 'MediaCT',
        'Zeo', 'De Nieuwe Zaak', 'Yellowlab', 'ISM eCompany', 'Kega', 'Guapa'
    ]
}


def filter_agency_positions(input_filepath, output_filepath):
    """
    Filter positions from specific digital agencies
    """
    try:
        print("Loading dataset...")
        df = pd.read_csv(input_filepath)

        # Original size
        original_size = len(df)
        print(f"\nOriginal dataset size: {original_size:,} rows")

        # Create list of all agencies
        all_agencies = []
        for category, agencies in DIGITAL_AGENCIES.items():
            all_agencies.extend(agencies)

        # Filter for agencies
        print("\nFiltering positions from digital agencies...")
        agency_mask = df['organizationname'].isin(all_agencies)
        filtered_df = df[agency_mask]

        # Get statistics
        filtered_size = len(filtered_df)
        print(f"\nFiltered dataset size: {filtered_size:,} rows")
        print(f"Removed {original_size - filtered_size:,} rows")

        # Show distribution by agency category
        print("\nDistribution by agency category:")
        for category, agencies in DIGITAL_AGENCIES.items():
            category_count = filtered_df[filtered_df['organizationname'].isin(agencies)].shape[0]
            if category_count > 0:
                print(f"\n{category}:")
                print(f"Total positions: {category_count}")

                # Show breakdown by agency within category
                agency_counts = filtered_df[filtered_df['organizationname'].isin(agencies)][
                    'organizationname'].value_counts()
                for agency, count in agency_counts.items():
                    print(f"- {agency}: {count:,} positions")

        # Show top position titles
        print("\nTop 20 position titles:")
        title_counts = filtered_df['positiontitle'].value_counts().head(20)
        for title, count in title_counts.items():
            print(f"- {title}: {count:,} positions")

        # Save filtered dataset
        print(f"\nSaving filtered dataset to {output_filepath}")
        filtered_df.to_csv(output_filepath, index=False)

        return filtered_df

    except Exception as e:
        print(f"Error during filtering: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def analyze_agency_positions(df):
    """
    Analyze the agency positions in detail
    """
    if df is not None and not df.empty:
        print("\n=== Agency Positions Analysis ===")

        # Analyze positions over time
        if 'datefound' in df.columns:
            print("\nPositions over time:")
            df['datefound'] = pd.to_datetime(df['datefound'], errors='coerce')
            year_counts = df['datefound'].dt.year.value_counts().sort_index()
            for year, count in year_counts.items():
                if not pd.isna(year):
                    print(f"Year {int(year)}: {count:,} positions")

        # Analyze education requirements
        if 'educationdegree' in df.columns:
            print("\nEducation requirements:")
            edu_counts = df['educationdegree'].value_counts()
            for edu, count in edu_counts.items():
                if pd.notna(edu):
                    print(f"{edu}: {count:,} positions")

        # Analyze geographical distribution
        if 'physicallocationprovince' in df.columns:
            print("\nGeographical distribution:")
            location_counts = df['physicallocationprovince'].value_counts()
            for location, count in location_counts.items():
                if pd.notna(location):
                    print(f"{location}: {count:,} positions")

        # Analyze position types
        if 'positiontitlegeneralized' in df.columns:
            print("\nTop 20 generalized position types:")
            position_counts = df['positiontitlegeneralized'].value_counts().head(20)
            for position, count in position_counts.items():
                print(f"- {position}: {count:,} positions")


if __name__ == "__main__":
    # File paths
    input_file = "/Users/dennishagen/Desktop/Verzameldocumenten master/dialogic_hu_2017_2021.csv"
    output_file = "/Users/dennishagen/Desktop/Verzameldocumenten master/digital_agency_positions.csv"

    # Filter the data
    filtered_df = filter_agency_positions(input_file, output_file)

    # Analyze the filtered data
    if filtered_df is not None:
        analyze_agency_positions(filtered_df)