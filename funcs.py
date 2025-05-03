import re

def txt_to_string_list(file_path: str, delim: list[str] = ['.', '?', '!', ';']) -> list[list[str]]:
    """
    Read a text file and split its content into a list of lists of strings by sentence delimiters.
    Punctuation is tokenized as separate strings.
    
    Args:
        file_path (str): Path to the input text file.
        delim (list[str]): List of delimiters to split sentences.
            Default is ['.', '?', '!'].

    Returns:
        list[list[str]]: A list of lists, where each inner list contains strings split by the specified delimiters.
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    tokens = re.findall(r'\w+|[^\w\s]', text)

    sentences = [[]]
    for token in tokens:
        if token in delim:
            sentences[-1].append(token)
            sentences.append([])
        else:
            sentences[-1].append(token)

    return sentences
