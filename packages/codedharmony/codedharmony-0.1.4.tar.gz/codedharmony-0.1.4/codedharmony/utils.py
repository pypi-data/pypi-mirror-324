def merge_dicts(*dicts):
    """
    Merge any number of dictionaries into a single dictionary.

    :param dicts: Variable number of dictionaries to merge
    :return: Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result

def safe_division(numerator, denominator, default=0):
    """
    Perform division safely; returns a default value if division by zero is attempted.

    :param numerator: The number to divide
    :param denominator: The number to divide by
    :param default: Value to return if division by zero
    :return: Result of division or default value
    """
    if denominator == 0:
        return default
    return numerator / denominator

def flatten_list(nested_list):
    """
    Flatten a nested list of any depth.

    :param nested_list: List that might contain other lists
    :return: A single flat list
    """
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

def chunk_list(lst, n):
    """
    Divide a list into chunks of size n.

    :param lst: The list to chunk
    :param n: Size of each chunk
    :return: List of lists where each inner list is a chunk
    """
    return [lst[i:i+n] for i in range(0, len(lst), n)]

def find_duplicates(lst):
    """
    Find and return duplicates in a list.

    :param lst: List to search for duplicates
    :return: List of duplicates
    """
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

def unique_elements(lst):
    """
    Return a list of unique elements from the input list.

    :param lst: Input list
    :return: List with unique elements
    """
    return list(dict.fromkeys(lst))

def camel_to_snake(s):
    """
    Convert a string from camelCase to snake_case.

    :param s: String in camelCase
    :return: String in snake_case
    """
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')

def snake_to_camel(s):
    """
    Convert a string from snake_case to camelCase.

    :param s: String in snake_case
    :return: String in camelCase
    """
    return ''.join(word.capitalize() if i else word for i, word in enumerate(s.split('_')))

def is_palindrome(s):
    """
    Check if a string is a palindrome, ignoring spaces, punctuation, and case.

    :param s: String to check
    :return: Boolean indicating if the string is a palindrome
    """
    import re
    s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return s == s[::-1]


def count_occurrences(lst):
    """
    Count occurrences of elements in a list.

    :param lst: List to count elements from
    :return: Dictionary where keys are list elements and values are their counts
    """
    return dict(Counter(lst))

def sort_dict_by_value(d, reverse=False):
    """
    Sort a dictionary by its values.

    :param d: Dictionary to sort
    :param reverse: If True, sort in descending order
    :return: Sorted list of tuples (key, value)
    """
    return sorted(d.items(), key=lambda x: x[1], reverse=reverse)

def remove_none_values(d):
    """
    Remove None values from a dictionary.

    :param d: Dictionary to clean
    :return: New dictionary without None values
    """
    return {k: v for k, v in d.items() if v is not None}

def list_to_dict(lst, key_func, value_func=None):
    """
    Convert list items to dictionary based on key and optional value functions.

    :param lst: List to convert
    :param key_func: Function to generate keys from list items
    :param value_func: Function to generate values from list items, default is None which uses the item itself
    :return: Dictionary created from list
    """
    if value_func is None:
        return {key_func(item): item for item in lst}
    return {key_func(item): value_func(item) for item in lst}