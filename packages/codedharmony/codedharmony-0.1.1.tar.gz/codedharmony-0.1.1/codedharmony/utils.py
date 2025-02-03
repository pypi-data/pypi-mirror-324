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
