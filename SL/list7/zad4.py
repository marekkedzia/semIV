def make_generator(f):
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1
    return generator()


def fibonacci(n):
    def fib_helper(n, memo):
        if memo[n] is None:
            memo[n] = fib_helper(n - 1, memo) + fib_helper(n - 2, memo)
        return memo[n]

    return None if n <= 0 else (0 if n == 1 else (1 if n == 2 else fib_helper(n, [None] * (n + 1))))


fib_gen = make_generator(fibonacci)
for i in range(10):
    print(next(fib_gen))

print("\n")

arith_seq_gen = make_generator(lambda n: 2 * n)
for i in range(10):
    print(next(arith_seq_gen))

print("\n")

geom_seq_gen = make_generator(lambda n: 2 ** n)
for i in range(10):
    print(next(geom_seq_gen))

print("\n")

power_seq_gen = make_generator(lambda n: n ** 2)
for i in range(10):
    print(next(power_seq_gen))

