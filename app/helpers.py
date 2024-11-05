import time

# Generate a random salt (you can adjust the length as needed)
import random

# Custom base encoding and decoding system

# Edit this list of characters as desired
BASE_ALPH = tuple("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
BASE_DICT = dict((c, v) for v, c in enumerate(BASE_ALPH))
BASE_LEN = len(BASE_ALPH)


def base_decode(string):
    """
    Decodes a given string from the custom base to a numerical value.

    Args:
        string (str): The input string to be decoded.

    Returns:
        int: The decoded numerical value.

    Raises:
        TypeError: If the input is not a string.
        ValueError: If the input string contains characters not in BASE_ALPH.
    """
    if not isinstance(string, str):
        raise TypeError("Input must be a string")

    try:
        num = 0
        for char in string:
            num = num * BASE_LEN + BASE_DICT[char]
        return num
    except KeyError as e:
        raise ValueError(f"Invalid character '{e.args[0]}' in input string")


def base_encode(num):
    """
    Encodes a given numerical value into a string using the custom base.

    Args:
        num (int): The input numerical value to be encoded.

    Returns:
        str: The encoded string.

    Raises:
        TypeError: If the input is not an integer.
    """
    if not isinstance(num, int):
        raise TypeError("Input must be an integer")

    if not num:
        return BASE_ALPH[0]

    encoding = ""
    while num:
        num, rem = divmod(num, BASE_LEN)
        encoding = BASE_ALPH[rem] + encoding
    return encoding


def generate_unique_id():
    """
    Generates a unique ID by combining the current system timestamp with a random salt.

    Returns:
        str: The unique ID encoded in the custom base.
    """
    # Get the current system timestamp in seconds since the epoch
    timestamp = int(time.time())

    salt = random.randint(1000, 9999)

    # Combine the timestamp and salt
    unique_num = (timestamp * 10000) + salt

    # Encode the unique number using the custom base
    unique_id = base_encode(unique_num)

    return unique_id


# Example usage:
if __name__ == "__main__":
    unique_id = generate_unique_id()
    print("Unique ID:", unique_id)
