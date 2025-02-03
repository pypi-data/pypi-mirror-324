from re import match, sub

TWO = 2
NUMBER_FOR_REST = 11
SIZE_CPF = 11
SIZE_CNPJ = 14
PATTERN = r'[.\-/]'

DIGITS = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 17,
    'B': 18,
    'C': 19,
    'D': 20,
    'E': 21,
    'F': 22,
    'G': 23,
    'H': 24,
    'I': 25,
    'J': 26,
    'K': 27,
    'L': 28,
    'M': 29,
    'N': 30,
    'O': 31,
    'P': 32,
    'Q': 33,
    'R': 34,
    'S': 35,
    'T': 36,
    'U': 37,
    'V': 38,
    'X': 39,
    'W': 40,
    'Y': 41,
    'Z': 42,
}

CPF = {
    'first_digit': [10, 9, 8, 7, 6, 5, 4, 3, 2],
    'second_digit': [11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
}

CNPJ = {
    'first_digit': [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
    'second_digit': [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
}

VALUE_PATTERN = (
    r'^[0-9]{11}$|^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$'
    r'|^[0-9A-Z]{14}$'
    '|^[0-9A-Z]{2}.[0-9A-Z]{3}.[0-9A-Z]{3}/[0-9A-Z]{4}-[0-9]{2}$'
)


def verify_pattern(value: str) -> bool:
    if bool(match(VALUE_PATTERN, value)):
        return True
    else:
        raise ValueError


def remove_punctuation(value: str) -> str:
    return sub(PATTERN, '', value)


def first_digit_cpf_checker_is_valid(value: str) -> bool:
    value = remove_punctuation(value)
    combinations = list(
        zip(CPF.get('first_digit'), [int(x) for x in value[:10]])
    )
    sum_ = 0
    for item in combinations:
        x, y = item
        sum_ += x * y
    rest_of_division = sum_ % NUMBER_FOR_REST
    result = (
        0 if rest_of_division < TWO else NUMBER_FOR_REST - rest_of_division
    )
    return result == int(value[9])


def second_digit_cpf_checker_is_valid(value: str) -> bool:
    value = remove_punctuation(value)
    combinations = list(
        zip(CPF.get('second_digit'), [int(x) for x in value[:11]])
    )
    sum_ = 0
    for item in combinations:
        x, y = item
        sum_ += x * y
    rest_of_division = sum_ % NUMBER_FOR_REST
    result = (
        0 if rest_of_division < TWO else NUMBER_FOR_REST - rest_of_division
    )
    return result == int(value[10])


def first_digit_cnpj_checker_is_valid(value: str) -> bool:
    value = remove_punctuation(value)
    combinations = list(
        zip(CNPJ.get('first_digit'), [int(DIGITS.get(x)) for x in value[:12]])
    )
    sum_ = 0
    for item in combinations:
        x, y = item
        sum_ += x * y
    rest_of_division = sum_ % NUMBER_FOR_REST
    result = (
        0 if rest_of_division < TWO else NUMBER_FOR_REST - rest_of_division
    )
    return result == int(value[12])


def second_digit_cnpj_checker_is_valid(value: str) -> bool:
    value = remove_punctuation(value)
    combinations = list(
        zip(CNPJ.get('second_digit'), [int(DIGITS.get(x)) for x in value[:13]])
    )
    sum_ = 0
    for item in combinations:
        x, y = item
        sum_ += x * y
    rest_of_division = sum_ % NUMBER_FOR_REST
    result = (
        0 if rest_of_division < TWO else NUMBER_FOR_REST - rest_of_division
    )
    return result == int(value[13])


def cnpj_or_cpf_is_valid(value: str) -> bool:
    result = False

    try:
        verify_pattern(value)

        value = remove_punctuation(value)

        if len(value) == SIZE_CPF and (
            first_digit_cpf_checker_is_valid(value)
            and second_digit_cpf_checker_is_valid(value)
        ):
            result = True
        if len(value) == SIZE_CNPJ and (
            first_digit_cnpj_checker_is_valid(value)
            and second_digit_cnpj_checker_is_valid(value)
        ):
            result = True
    except ValueError:
        result = False
    return result
