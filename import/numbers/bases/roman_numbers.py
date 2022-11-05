# Roman conversion "decimal to roman"
def to_roman(number: int) -> str:
    """ Converts decimal number to roman number

    Args:
        number (int): Decimal number to be converted.

    Returns:
        int: Roman number converted from decimal number.
    """
    values = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
    symbols = ["I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M"]
    i = len(values) - 1
    ret = ""
    while number > 0:
        division = number // values[i]
        number = number % values[i]
        while division:
            division -= 1
            ret += symbols[i]
        i-=1
    return ret
