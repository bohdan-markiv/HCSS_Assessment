import re
import os


def contains_keyword(text, keywords):
    """
    Check if the given text contains any of the keywords as whole words.

    Parameters:
    - text (str): The text to analyze.
    - keywords (list of str): The pool of keywords to search for.

    """
    for keyword in keywords:
        # Create a regex pattern with word boundaries to match unique words.
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def process_text_line(line, keywords):
    """
    Process a single line of text that is assumed to be separated into two columns.

    Parameters:
    - line (str): The line to process.
    - keywords (list of str): The pool of keywords to check in the second column.

    """
    # Use split with maxsplit=1 to split on any whitespace.
    parts = line.split(None, 1)
    # Ensure there are at least two parts: identifier and text.
    if len(parts) < 2:
        return False
    text = parts[1]
    return contains_keyword(text, keywords)


def process_file(file_path, keywords):
    """
    Read the file and analyze each line for the presence of keywords as unique words in the second column.

    Parameters:
    - file_path (str): Path to the text file.
    - keywords (list of str): The pool of keywords to check.
    """
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Remove any leading/trailing whitespace.
            line = line.strip()
            # Skip empty lines.
            if not line:
                continue
            flag = process_text_line(line, keywords)
            results.append((line, flag))
    return results


def get_documents(topics):
    """
    Scans all .txt files in a speeches folder and returns a list of file paths 
    that contain at least one match from the keywords_pool.

    Returns:
        List[str]: A list of file paths where relevant keywords were found.
    """
    # Replace with the actual file path
    folder_path = "data/year_2022/txt/2022"
    all_files = [x for x in os.listdir(folder_path) if x.endswith(".txt")]
    files_with_reaim = []
    for file in all_files:
        file_path = folder_path + "/" + file
        results = process_file(file_path, topics)

        # Output the results
        for line, found in results:
            if found:
                files_with_reaim.append(file_path)
                continue

    return files_with_reaim
