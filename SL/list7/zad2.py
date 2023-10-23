def for_all(predicate, input_iterable):
    return all(map(predicate, input_iterable))


def exists(predicate, input_iterable):
    return any(map(predicate, input_iterable))


def at_least(min_count, predicate, input_iterable):
    return sum(map(predicate, input_iterable)) >= min_count


def at_most(max_count, predicate, input_iterable):
    return sum(map(predicate, input_iterable)) <= max_count
