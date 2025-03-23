from process_data import get_documents
import pandas as pd
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


def prepare_full_tables(topics):
    """
    Loads, filters, and enriches speech and metadata tables based on selected topics.

    This function:
    - Loads speeches and their metadata using `get_tables()`.
    - Converts the input topic list into regex patterns for flexible matching.
    - Filters speeches that mention at least one of the topics.
    - Applies VADER sentiment analysis to those relevant speeches.
    - Enriches the dataset with speaker attributes such as age, gender, and month of speech.

    Args:
        topics (List[str]): A list of topic keywords to search for in speeches.
    """
    # Make sure to download the VADER lexicon if not already present
    nltk.download('vader_lexicon')

    df, meta = get_tables(topics=topics)
    keywords = []
    # Expanded list of keywords (using regex patterns)
    for topic in topics:
        if topic in ["military technology", "defense technology"]:
            base = topic.replace(" technology", "")
            keywords.append(rf"\b{base} technolog(?:y|ies)?\b")
        elif topic == "neural network":
            keywords.append(r"\bneural network(?:s)?\b")
        elif topic == "drone":
            keywords.append(r"\bdrones?\b")
        else:
            keywords.append(rf"\b{topic}\b")

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

    # Create columns with sentiment scores
    df = df.reset_index().drop(columns=["index"])
    sentiment_expanded = df['sentiment'].apply(pd.Series)

    # Join these new columns to the original DataFrame
    df = df.join(sentiment_expanded)
    df = df.drop(columns=["sentiment"])
    df[df['contains_topic'] == True]

    # Drop duplicates and combine in one dataframe
    meta = meta.drop_duplicates(subset=["ID"])
    df = df.drop_duplicates(subset=["ID"])
    combined = pd.merge(df, meta, on="ID", how="left")

    contained_df = combined[combined["contains_topic"]
                            == True].reset_index().drop(columns=["index"])

    # Add several new columns for the further analysis
    contained_df["Age"] = 2022 - \
        pd.to_numeric(contained_df["Speaker_birth"], errors="coerce")
    contained_df["is_female"] = contained_df["Speaker_gender"] == "F"
    contained_df['Month'] = contained_df['Date'].apply(
        lambda x: int(x.split('-')[1]))

    return contained_df


def get_tables(topics):
    """
    Loads and processes speech documents and their corresponding metadata files 
    based on the presence of specific topic keywords.

    Args:
        topics (List[str]): A list of topic-related keywords to search for in the documents.

    """
    documents = get_documents(topics=topics)

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
