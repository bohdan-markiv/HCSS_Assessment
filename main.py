from prepare_tables import prepare_full_tables
import pandas as pd


def get_data(key_words: list, save_as_csv=True):
    """Simple function which creates the dataframe for the further analysis, based on the selected pool of key words.
    Can either return a pandas dataframe, or save the file in the local data folder. 

    Args:
        key_words (list): List of the key words, which are attributed to the topic of interest
        save_as_csv (bool, optional): The checker which identifies if the user wants to save the file locally
        or use it further within the script. Defaults to True.
    """
    df = prepare_full_tables(topics=key_words)
    if save_as_csv:
        df.to_csv("data/prepared_tables.csv")
        return ("File saved.")
    else:
        return df


if __name__ == "__main__":
    key_words = [
        "reaim",
        "reaim summit",
        "artificial intelligence",
        "ai",
        "military technology",
        "defense technology",
        "machine learning",
        "deep learning",
        "neural network",
        "drone",
        "military"]
    get_data(key_words, save_as_csv=True)
