def count_decimal_places(number_string):

    # Find the index of the decimal point
    decimal_index = number_string.find('.')

    # If there is no decimal point, return 0
    if decimal_index == -1:
        return 0

    # Otherwise, return the number of digits after the decimal point
    return len(number_string) - decimal_index - 1