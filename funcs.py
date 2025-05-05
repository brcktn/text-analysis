import re
import os
import openai


def get_api_key() -> str:
    """
    Retrieve the API key from an environment variable.

    Returns:
        str: The API key.
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable is not set.")
    return api_key


def txt_to_string_list(
    file_path: str, delim: list[str] = [".", "?", "!", ";"]
) -> list[list[str]]:
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

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().lower()

    tokens = re.findall(r"\w+|[^\w\s]", text)

    sentences = [[]]
    for token in tokens:
        if token in delim:
            sentences[-1].append(token)
            sentences.append([])
        else:
            sentences[-1].append(token)

    return sentences


def phrase_frequency(
    sentences: list[list[str]], phrase_len: int
) -> list[tuple[str, int]]:
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
            phrase = " ".join(sentence[i : i + phrase_len])
            if phrase in phrase_freq:
                phrase_freq[phrase] += 1
            else:
                phrase_freq[phrase] = 1

    return sorted(phrase_freq.items(), key=lambda x: x[1], reverse=True)


def next_word_frequency(
    sentences: list[list[str]], word: str
) -> list[tuple[str, float]]:
    """
    Calculate the frequencies of words following a specific word in a list of sentences.

    Args:
        sentences (list[list[str]]): A list of lists, where each inner list contains strings.
        word (str): The word to calculate the next word probabilities for.

    Returns:
        list[tuple(str, float)]: A list of tuples, where each tuple contains a word and its number of occurences.
    """

    next_word_freq = {}
    total_count = 0

    for sentence in sentences:
        for i in range(len(sentence) - 1):
            if sentence[i] == word:
                next_word = sentence[i + 1]
                if next_word in next_word_freq:
                    next_word_freq[next_word] += 1
                else:
                    next_word_freq[next_word] = 1
                total_count += 1

    return sorted(next_word_freq.items(), key=lambda x: x[1], reverse=True)


def word_frequency_given_word(
    sentences: list[list[str]], word: str
) -> list[tuple[str, int]]:
    """
    Count the frequency of words only in sentences that contain a specific word.

    Args:
        sentences (list[list[str]]): A list of lists, where each inner list contains strings.
        word (str): The word to filter sentences by.
    Returns:
        list[tuple(str, int)]: A list of tuples, where each tuple contains a word and its frequency.
    """

    word_freq = {}

    for sentence in sentences:
        if word in sentence:
            for w in sentence:
                if w in word_freq:
                    word_freq[w] += 1
                else:
                    word_freq[w] = 1

    return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)


def most_important_words(
    sentences: list[list[str]],
    input_file: str,
    ) -> list[tuple[str, int]]:
    """
    Uses OpenAI's GPT-4.1 nano to identify the most important word in each line of a text file.
    Args:
        sentences (list[list[str]]): A list of lists, where each inner list contains strings.
        input_file (str): The path to the input text file.
    Returns:
        list[tuple(str, int)]: A list of tuples, where each tuple contains a word and its frequency.
    """

    openai.api_key = get_api_key()

    important_words = {}

    with open(input_file, "r", encoding="utf-8") as file:
        text = file.readlines()
        for line in text:
            response = openai.ChatCompletion.create(
                model="gpt-4.1-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"Identify the most important word in the following sentence: {line}",
                    }
                ],
            )
            important_word = response["choices"][0]["message"]["content"].strip()
            if important_word in important_words:
                important_words[important_word] += 1
            else:
                important_words[important_word] = 1




