import re

def txt_to_string_list(file_path: str, delim: list[str] = ['.', '?', '!', ';']) -> list[list[str]]:
    """
    Read a text file and split its content into a list of lists of strings by sentence delimiters.
    Punctuation is tokenized as separate strings, and all text is converted to lowercase.
    
    Args:
        file_path (str): Path to the input text file.
        delim (list[str]): List of delimiters to split sentences.
            Default is ['.', '?', '!'].

    Returns:
        list[list[str]]: A list of lists, where each inner list contains strings split by the specified delimiters.
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()

    tokens = re.findall(r'\w+|[^\w\s]', text)

    sentences = [[]]
    for token in tokens:
        if token in delim:
            sentences[-1].append(token)
            sentences.append([])
        else:
            sentences[-1].append(token)

    return sentences


def phrase_frequency_list(sentences: list[list[str]], phrase_len: int) -> list[tuple[str, int]]:
    """
    Count the frequency of phrases of a given length in a list of sentences.

    Args:
        sentences (list[list[str]]): A list of lists, where each inner list contains strings.
        phrase_len (int): The length of the phrases to count.

    Returns:
        set[tuple(str, int)]: A set of tuples, where each tuple contains a phrase and its frequency.
    """
    
    phrase_freq = {}
    
    for sentence in sentences:
        if len(sentence) < phrase_len:
            continue
        for i in range(len(sentence) - phrase_len + 1):
            phrase = ' '.join(sentence[i:i + phrase_len])
            if phrase in phrase_freq:
                phrase_freq[phrase] += 1
            else:
                phrase_freq[phrase] = 1

    return sorted(phrase_freq.items(), key=lambda x: x[1], reverse=True)
