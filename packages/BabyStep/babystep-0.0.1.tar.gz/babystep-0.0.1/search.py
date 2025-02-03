import re

def search_bylinear(arr, target):
    """Performs linear search on the list to find the target."""
    for i, element in enumerate(arr):
        if element == target:
            return i  # Return the index of the target element
    return "Not found"  # return "Not found" if target is not found


def search_bybinary(arr, target):
    """Performs binary search on a sorted list to find the target."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid  # Return the index of the target element
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return "Not found"  # return "Not found" if target is not found


def search_bystring(text, substring):
    """Search for a substring in a string and return the index."""
    return text.find(substring)  # Returns -1 if not found, otherwise returns the index


def search_byindexofelement(arr, target):
    """Finds the index of a target element in a list or string."""
    try:
        return arr.index(target)  # Returns the index of the element
    except ValueError:
        return "Not found"  # Returns -1 if the target is not found


def search_indict(d, key):
    """Search for a key in the dictionary."""
    if key in d:
        return d[key]  # Return the value associated with the key
    return None  # Return None if the key is not found


def search_inlistofdicts(lst, key, value):
    """Search for a key-value pair in a list of dictionaries."""
    for i, d in enumerate(lst):
        if d.get(key) == value:
            return i  # Return index if found
    return "Not found"  # return "Not found" if not found


def find_alloccurrences(arr, target):
    """Find all occurrences of a target element in a list or string."""
    return [i for i, element in enumerate(arr) if element == target]


def search_bypattern(text, pattern):
    """Search for a pattern using regular expressions."""
    matches = re.finditer(pattern, text)
    return [match.start() for match in matches]  # Returns the starting indices of all matches


# # Example Usage:
# if __name__ == "__main__":
#     # Example List
#     arr = [1, 2, 3, 4, 5]
#     arr_sorted = [1, 2, 3, 4, 5]

#     # Linear Search Example
#     print(linear_search(arr, 3))  # Output: 2

#     # Binary Search Example (Sorted Array)
#     print(binary_search(arr_sorted, 4))  # Output: 3

#     # String Search Example
#     text = "Hello, world!"
#     print(string_search(text, "world"))  # Output: 7

#     # Index Search Example
#     print(index_of_element(arr, 5))  # Output: 4

#     # Dictionary Search Example
#     d = {"apple": 1, "banana": 2, "cherry": 3}
#     hint = "banana"
#     print(search_in_dict(d,hint))# Output: 2

#     # List of Dictionaries Search Example
#     lst_of_dicts = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
#     print(search_in_list_of_dicts(lst_of_dicts, "name", "Bob"))  # Output: 1

#     # Multiple Occurrences Search Example
#     text = "abacab"
#     hint = 'a'
#     print(find_all_occurrences(text, hint))  # Output: [0, 3, 5]

#     # # Regex Search Example
#     text = "abc 123 abc 456"
#     pattern = r"\d+"
#     print(regex_search(text, pattern))  # Output: [4, 12]


def search_bymatch(text, pattern):
    """
    Check if the pattern matches at the start of the string.
    
    Args:
    - text (str): The string to check for the pattern.
    - pattern (str): The pattern to match at the start of the string.
    
    Returns:
    - str: The matched string, or "No match at the start" if the pattern doesn't match at the start.
    """
    match = re.match(pattern, text)
    if match:
        return match.group()
    return "No match at the start"

def search_findall(text, pattern):
    """
    Find all non-overlapping matches of a pattern in the given text.
    
    Args:
    - text (str): The string to search for all matches.
    - pattern (str): The pattern to search for.
    
    Returns:
    - list: A list of all match groups found.
    """
    return [match.group() for match in re.finditer(pattern, text)]

def split_bypattern(text, pattern):
    """
    Split the text by occurrences of the pattern.
    
    Args:
    - text (str): The string to split.
    - pattern (str): The pattern by which to split the string.
    
    Returns:
    - list: A list of strings resulting from the split.
    """
    return re.split(pattern, text)

def search_byfullmatch(text, pattern):
    """
    Check if the entire string matches the pattern.
    
    Args:
    - text (str): The string to check for a full match.
    - pattern (str): The pattern to match against the entire string.
    
    Returns:
    - str: The matched string, or "No full match" if the entire string does not match the pattern.
    """
    match = re.fullmatch(pattern, text)
    if match:
        return match.group()
    return "No full match"

def extract_bygroups(text, pattern):
    """
    Extract captured groups from the text using the given pattern.
    
    Args:
    - text (str): The string to extract groups from.
    - pattern (str): The pattern with capture groups to extract.
    
    Returns:
    - tuple: A tuple of captured groups, or "No match" if no match is found.
    """
    match = re.search(pattern, text)
    if match:
        return match.groups()
    return "No match"

def search_withposition(text, pattern):
    """
    Search for a pattern and return its position in the string.
    
    Args:
    - text (str): The string to search for the pattern.
    - pattern (str): The pattern to search for.
    
    Returns:
    - tuple: A tuple containing the start and end position of the match, or "No match" if no match is found.
    """
    match = re.search(pattern, text)
    if match:
        return match.start(), match.end()
    return "No match"

def replace_bypattern(text, pattern, replacement):
    """
    Substitute the occurrences of a pattern with a replacement string.
    
    Args:
    - text (str): The string in which to substitute the pattern.
    - pattern (str): The pattern to find.
    - replacement (str): The string to replace the pattern with.
    
    Returns:
    - str: The modified string with the pattern replaced by the replacement.
    """
    return re.sub(pattern, replacement, text)

def search_bycase_insensitive(text, pattern):
    """
    Perform a case-insensitive search for a pattern in the text.
    
    Args:
    - text (str): The string in which to search for the pattern.
    - pattern (str): The pattern to search for.
    
    Returns:
    - str: The matched pattern, or "No match found" if no match is found.
    """
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group()
    return "No match found"

def search_byoptionalpattern(text, pattern):
    """
    Search for an optional pattern in the string.
    
    Args:
    - text (str): The string to search for the pattern.
    - pattern (str): The pattern with optional parts to search for.
    
    Returns:
    - str: The matched pattern, or "No match found" if no match is found.
    """
    match = re.search(pattern, text)
    if match:
        return match.group()
    return "No match found"



# print(match_search("Hello, world!", r"Hello"))  # Hello
# print(find_all_matches("abc 123 abc 456", r"abc"))  # ['abc', 'abc']
# print(split_by_pattern("apple, orange, banana", r",\s*"))  # ['apple', 'orange', 'banana']
# print(full_match_search("12345", r"\d+"))  # 12345
# print(extract_groups("Order number: 12345, Quantity: 100", r"Order number: (\d+), Quantity: (\d+)"))  # ('12345', '100')
# print(search_with_position("abc 123 abc 456", r"\d+"))  # (4, 7)
# print(substitute_pattern("abc 123 abc 456", r"\d+", "XXX"))  # abc XXX abc XXX
# print(case_insensitive_search("Hello, World!", r"world"))  # World
# print(optional_pattern_search("ac", r"ab?c"))  # ac
