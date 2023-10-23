from functools import reduce


def acronym(words):
    return reduce(lambda acc, word: acc + word[0].upper(), words, '')


def median(numbers):
    sorted_numbers = sorted(numbers)
    numbers_count = len(sorted_numbers)
    middle = numbers_count // 2

    def is_even_length():
        return numbers_count % 2 == 0

    def count_average(x, y):
        return x + y / 2

    return count_average(sorted_numbers[middle - 1], sorted_numbers[middle + 1]) if is_even_length() else \
        sorted_numbers[middle]


def sqrt_newton(x, epsilon):
    def is_within_tolerance(y):
        return abs(y**2 - x) < epsilon

    def sqrt_newton_rec(y):
        next_y = (y + x / y) / 2
        return y if is_within_tolerance(y) else sqrt_newton_rec(next_y)

    return sqrt_newton_rec(x)


def make_alpha_dict(input):
    def get_unique_chars(string):
        return sorted(set(char for char in string if char.isalpha()))

    def filter_words_containing_char(words, char):
        return [word for word in words if char in word]

    def update_alpha_dict(acc, char):
        return {**acc, char: filter_words_containing_char(words_list, char)}

    words_list = input.split()
    unique_chars = get_unique_chars(input)

    return {char: update_alpha_dict({}, char) for char in unique_chars}


def flatten(input_list):
    def is_scalar(item):
        return not isinstance(item, (list, tuple))

    def process_element(element):
        return flatten_recursive(element) if not is_scalar(element) else [element]

    def flatten_recursive(seq):
        return [x for element in seq for x in process_element(element)]

    return flatten_recursive(input_list)

