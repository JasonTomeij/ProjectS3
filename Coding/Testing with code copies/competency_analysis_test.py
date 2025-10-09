import pandas as pd
import spacy
import numpy as np
from collections import Counter
from bs4 import BeautifulSoup
import re
from datetime import datetime
from keybert import KeyBERT


def filter_recent_descriptions(df):
    """Filter descriptions from 2020 onwards using datefound"""
    print("Filtering descriptions from 2020 onwards...")

    # Convert datefound to datetime
    df['datefound'] = pd.to_datetime(df['datefound'], errors='coerce')

    # Filter for dates >= 2020
    cutoff_date = pd.Timestamp('2020-01-01')
    recent_df = df[df['datefound'] >= cutoff_date].copy()

    print(f"Original dataset size: {len(df):,} descriptions")
    print(f"Filtered dataset size (2020+): {len(recent_df):,} descriptions")

    # Show distribution by year
    year_counts = recent_df['datefound'].dt.year.value_counts().sort_index()
    print("\nDistribution by year:")
    for year, count in year_counts.items():
        print(f"{year}: {count:,} descriptions")

    return recent_df


class CompetencyExtractor:
    def __init__(self):
        """Initialize the competency extractor with necessary models and dictionaries"""
        print("Loading NLP models...")
        self.nlp_nl = spacy.load("nl_core_news_lg")
        self.kw_model = KeyBERT()

        # Define competency categories
        self.competency_categories = {
            'technical_marketing': [
                # English terms
                'digital marketing', 'social media', 'content marketing', 'seo', 'sea',
                'google analytics', 'data analysis', 'marketing automation', 'crm',
                'email marketing', 'growth hacking', 'conversion optimization',
                # Dutch terms
                'digitale marketing', 'sociale media', 'contentmarketing', 'zoekmachine optimalisatie',
                'e-mailmarketing', 'marketing automatisering', 'klantrelatiebeheer',
                'conversie optimalisatie', 'online marketing', 'digitale strategie',
                'webanalytics', 'digitale advertising', 'performance marketing',
                'marketing technologie', 'datagedreven marketing'
            ],
            'data_analytics': [
                # English & Dutch terms
                'sql', 'python', 'tableau', 'power bi', 'data visualization',
                'predictive analytics', 'statistical analysis', 'segmentation',
                'dataanalyse', 'data visualisatie', 'voorspellende analyse',
                'statistische analyse', 'klantensegmentatie', 'rapportages',
                'dashboards', 'data-analyse', 'klantinzichten', 'big data',
                'machine learning', 'data science', 'a/b testing', 'google tag manager',
                'google data studio', 'excel', 'spss', 'powerpoint'
            ],
            'strategic_skills': [
                # English & Dutch terms
                'strategische planning', 'marktonderzoek', 'concurrentieanalyse',
                'merkmanagement', 'productmarketing', 'go-to-market strategie',
                'customer journey', 'klantreis', 'waardepropositie',
                'positionering', 'marketingstrategie', 'businessontwikkeling',
                'strategisch inzicht', 'commercieel inzicht', 'marktinzicht',
                'stakeholder management', 'budgetbeheer', 'roi'
            ],
            'creative_skills': [
                # English & Dutch terms
                'content creatie', 'copywriting', 'storytelling', 'visueel ontwerp',
                'videoproductie', 'creative direction', 'creatieve richting',
                'merkidentiteit', 'gebruikerservaring', 'grafisch ontwerp',
                'adobe creative suite', 'photoshop', 'indesign', 'illustrator',
                'wordpress', 'cms', 'videobewerking', 'fotografie'
            ],
            'ai_tools': [
                # English & Dutch terms
                'chatgpt', 'midjourney', 'dall-e', 'kunstmatige intelligentie',
                'generatieve ai', 'ai copywriting', 'ai content', 'ai marketing',
                'prompt engineering', 'ai automatisering', 'machine learning marketing',
                'predictive modeling', 'ai strategie', 'ai implementatie'
            ],
            'soft_skills': [
                # Dutch terms
                'leiderschap', 'communicatie', 'samenwerking', 'projectmanagement',
                'agile', 'scrum', 'stakeholdermanagement', 'presentatievaardigheden',
                'analytisch denken', 'probleemoplossend vermogen', 'innovatie',
                'teamwork', 'timemanagement', 'plannen en organiseren',
                'zelfstandig werken', 'resultaatgericht', 'klantgericht',
                'overtuigingskracht', 'ondernemerschap', 'flexibiliteit'
            ],
            'languages': [
                'nederlands', 'english', 'duits', 'frans',
                'dutch', 'german', 'french',
                'moedertaal', 'vloeiend', 'uitstekende beheersing'
            ]
        }

        # Latest marketing trends in Dutch
        self.latest_trends = [
            'first-party data strategie',
            'privacy-first marketing',
            'ai-gedreven marketing automatisering',
            'generatieve ai implementatie',
            'zero-party data verzameling',
            'contextuele advertenties',
            'social commerce',
            'marketing in het metaverse',
            'voice search optimalisatie',
            'verantwoord ai-gebruik',
            'duurzaamheidsmarketing',
            'influencer marketing automatisering',
            'realtime personalisatie',
            'crossplatform attributie',
            'klantgegevensplatform beheer',
            'marketing automation platform',
            'customer data platform',
            'privacywetgeving',
            'gdpr compliance',
            'cookieless tracking'
        ]

    def clean_text(self, html_text):
        """Clean HTML and prepare text for analysis"""
        if pd.isna(html_text):
            return ""

        # Remove HTML tags
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text()
        text = re.sub(r'\s+', ' ', text)
        return text.lower().strip()

    def extract_competencies(self, text):
        """Extract competencies using multiple techniques"""
        competencies = []
        clean_text = self.clean_text(text)

        # Rule-based matching for known competencies
        for category, skills in self.competency_categories.items():
            for skill in skills:
                if skill in clean_text:
                    competencies.append({
                        'competency': skill,
                        'category': category,
                        'method': 'rule-based'
                    })

        # Check for latest trends
        for trend in self.latest_trends:
            if trend in clean_text:
                competencies.append({
                    'competency': trend,
                    'category': 'latest_trends',
                    'method': 'trend_matching'
                })

        return competencies

    def analyze_descriptions(self, df, sample_size=5000):
        """Analyze a sample of job descriptions and extract competencies"""
        print(f"Analyzing {sample_size} job descriptions...")

        # Take a random sample
        sample_df = df.sample(n=min(sample_size, len(df)), random_state=42)
        processed_df = sample_df.copy()

        # Initialize empty competencies column
        processed_df['competencies'] = None

        # Process descriptions with progress updates
        total_descriptions = len(processed_df)
        competencies_list = []  # Store all competencies here first

        print("Extracting competencies...")
        for idx, row in enumerate(processed_df.iterrows(), 1):
            if idx % 100 == 0:  # Progress update every 100 descriptions
                print(
                    f"Processing description {idx} of {total_descriptions}... ({(idx / total_descriptions) * 100:.1f}%)")

            comps = self.extract_competencies(row[1]['selectedtextincludinghtml'])
            competencies_list.append(comps)

        # Assign all competencies at once
        processed_df['competencies'] = competencies_list

        # Analyze competency trends
        print("\nAnalyzing competency trends...")
        all_competencies = []
        for comp_list in processed_df['competencies']:
            if isinstance(comp_list, list):  # Check if comp_list is valid
                all_competencies.extend([c['competency'] for c in comp_list])

        comp_counter = Counter(all_competencies)

        # Print results
        print("\n=== Competency Analysis Results ===")
        print(f"Total job descriptions analyzed: {len(processed_df):,}")
        print(f"Total competencies found: {len(all_competencies):,}")
        print(f"Average competencies per description: {len(all_competencies) / len(processed_df):.1f}")

        # Overall top competencies
        print("\nTop 50 most mentioned competencies:")
        for comp, count in comp_counter.most_common(50):
            percentage = (count / len(processed_df)) * 100
            print(f"{comp}: {count:,} mentions ({percentage:.1f}% of job posts)")

        # Analyze by category
        print("\n=== Competencies by Category ===")
        category_counts = Counter()
        for comp_list in processed_df['competencies']:
            if isinstance(comp_list, list):  # Check if comp_list is valid
                categories = [c['category'] for c in comp_list]
                category_counts.update(categories)

        for category, count in category_counts.most_common():
            percentage = (count / len(processed_df)) * 100
            print(f"{category}: {count:,} mentions ({percentage:.1f}% of job posts)")

        return processed_df


if __name__ == "__main__":
    # File paths
    input_file = "/Users/dennishagen/Desktop/Verzameldocumenten master/digital_agency_positions.csv"
    output_file = "/Users/dennishagen/Desktop/Verzameldocumenten master/marketing_positions_2020_digital_agencies.csv" #

    # Load and filter dataset
    print("Loading dataset...")
    df = pd.read_csv(input_file)
    recent_df = filter_recent_descriptions(df)

    # Initialize and run analysis
    extractor = CompetencyExtractor()
    df_with_competencies = extractor.analyze_descriptions(recent_df, sample_size=5000)

    # Save results
    df_with_competencies.to_csv(output_file, index=False)
    print(f"\nResults saved to {output_file}")

    # Print some additional statistics
    print("\n=== Additional Statistics ===")
    print("\nCompetencies per job title type:")
    job_types = df_with_competencies['positiontitlegeneralized'].value_counts().head(10)
    for job_type, count in job_types.items():
        jobs_df = df_with_competencies[df_with_competencies['positiontitlegeneralized'] == job_type]
        avg_competencies = sum(len(c) for c in jobs_df['competencies']) / len(jobs_df)
        print(f"\n{job_type} ({count:,} positions):")
        print(f"Average competencies per position: {avg_competencies:.1f}")