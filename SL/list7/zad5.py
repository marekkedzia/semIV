import functools


def make_generator_mem(f):
    @functools.lru_cache(maxsize=None)
    def memoized_f(n):
        return f(n)

    def generator():
        n = 1
        while True:
            yield memoized_f(n)
            n += 1
    return generator()


def fibonacci(n):
    def fib_helper(n, memo):
        memo[n] = memo[n] if memo[n] is not None else fib_helper(n - 1, memo) + fib_helper(n - 2, memo)
        return memo[n]

    return None if n <= 0 else (0 * (n == 1) + 1 * (n == 2) or fib_helper(n, [None] * (n + 1)))

fib_gen = make_generator_mem(fibonacci)
for i in range(10):
    print(next(fib_gen))
