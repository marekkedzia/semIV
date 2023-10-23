import logging
import functools
import time


def log(level):
    return lambda func: functools.wraps(func)(lambda *args, **kwargs: log_wrapper(level, func, *args, **kwargs))


def log_wrapper(level, func, *args, **kwargs):
    logger = logging.getLogger(func.__name__)
    logger.setLevel(level)

    start_time = time.time()
    result = func(*args, **kwargs)
    duration = time.time() - start_time

    args_str = ', '.join(repr(arg) for arg in args)
    kwargs_str = ', '.join(f"{key}={value!r}" for key, value in kwargs.items())
    signature = ', '.join(filter(None, [args_str, kwargs_str]))

    logger.log(level, f"Function {func.__name__} called with arguments: {signature}. "
                      f"Returned {result}. Took {duration:.6f} seconds.")
    return result


@log(logging.DEBUG)
def example_function(x, y):
    return x + y


@log(logging.INFO)
class ExampleClass:
    def __init__(self, name):
        self.name = name


example_function(3, 4)
example_instance = ExampleClass('example')
