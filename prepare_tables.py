from process_data import get_documents
import pandas as pd
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


def get_tables():

    documents = get_documents()

    df_speeches, df_meta = pd.DataFrame(), pd.DataFrame()

    for document in documents:

        results = []
        with open(document, 'r', encoding='utf-8') as file:
            for line in file:
                # Remove any leading/trailing whitespace.
                line = line.strip()
                # Skip empty lines.
                if not line:
                    continue
                line = line.split('\t')
                results.append(line)

        df_speeches_one = pd.DataFrame(results)

        df_speeches = pd.concat([df_speeches, df_speeches_one])

        meta_name = document.replace('.txt', '-meta.tsv')
        meta_result = []
        with open(meta_name, 'r', encoding='utf-8') as file:
            for line in file:
                # Remove any leading/trailing whitespace.
                line = line.strip()
                # Skip empty lines.
                if not line:
                    continue
                line = line.split('\t')
                meta_result.append(line)

        df_meta_one = pd.DataFrame(meta_result).T.set_index(0).T

        df_meta = pd.concat([df_meta, df_meta_one])

    df_speeches.columns = ['ID', 'Text']
    return df_speeches, df_meta


def prepare_full_tables():

    # Make sure to download the VADER lexicon if not already present
    nltk.download('vader_lexicon')

    df, meta = get_tables()

    # Expanded list of keywords (using regex patterns)
    keywords = [
        r'\breaim\b',                    # "reaim"
        r'\breaim summit\b',             # "reaim summit"
        r'\bartificial intelligence\b',  # exact phrase
        r'\bai\b',                       # "ai" as a whole word
        # military technology or technologies
        r'\bmilitary technolog(?:y|ies)?\b',
        # defense technology or technologies
        r'\bdefense technolog(?:y|ies)?\b',
        # Expanded topics:
        r'\bmachine learning\b',         # machine learning
        r'\bdeep learning\b',            # deep learning
        r'\bneural network(?:s)?\b',      # neural network or networks
        r'\bdrones?\b',                  # drone or drones
        # autonomous (often linked with military tech)
        r'\bautonomous\b',
        r'\bcyber warfare\b',
        r'\bmilitary\b'
    ]

    # Combine all keywords into one regular expression (case-insensitive)
    pattern = re.compile("|".join(keywords), re.IGNORECASE)

    # Define a function to check if any of the keywords is present in a given text

    def contains_topic(text):
        return bool(pattern.search(text))

    # Apply the checker function to the DataFrame's 'Text' column
    df['contains_topic'] = df['Text'].apply(contains_topic)

    # Initialize the VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Function to compute sentiment scores for a given text

    def get_sentiment(text):
        return sia.polarity_scores(text)

    # Apply sentiment analysis only for rows that contain topics; others get None.
    df['sentiment'] = df.apply(
        lambda row: get_sentiment(
            row['Text']) if row['contains_topic'] else None,
        axis=1
    )

    df = df.reset_index().drop(columns=["index"])
    sentiment_expanded = df['sentiment'].apply(pd.Series)

    # Join these new columns to the original DataFrame
    df = df.join(sentiment_expanded)
    df = df.drop(columns=["sentiment"])
    df[df['contains_topic'] == True]

    meta = meta.drop_duplicates(subset=["ID"])
    df = df.drop_duplicates(subset=["ID"])
    combined = pd.merge(df, meta, on="ID", how="left")

    contained_df = combined[combined["contains_topic"]
                            == True].reset_index().drop(columns=["index"])

    contained_df["Age"] = 2022 - \
        pd.to_numeric(contained_df["Speaker_birth"], errors="coerce")
    contained_df["is_female"] = contained_df["Speaker_gender"] == "F"
    contained_df['Month'] = contained_df['Date'].apply(
        lambda x: int(x.split('-')[1]))
    return contained_df
