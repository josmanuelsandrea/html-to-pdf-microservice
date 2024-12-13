def add_dots_to_number(number):
    """
    Adds a dot every three digits in the given number.

    Parameters:
        number (int or str): The input number (int or string format).

    Returns:
        str: The formatted string with dots every three digits.
    """
    if not isinstance(number, (int, str)):
        raise ValueError("Input must be an integer or a string representation of a number.")

    # Convert to string if the input is an integer
    number_str = str(number)

    # Check for negative numbers and handle sign
    if number_str.startswith("-"):
        is_negative = True
        number_str = number_str[1:]
    else:
        is_negative = False

    # Reverse the number string, insert dots, and reverse back
    reversed_with_dots = ".".join([number_str[max(i - 3, 0):i][::-1] for i in range(len(number_str), 0, -3)])
    formatted_number = reversed_with_dots[::-1]

    return "-" + formatted_number if is_negative else formatted_number