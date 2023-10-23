import random
import string


class PasswordGenerator:
    def __init__(self, length, count, charset=None):
        self.length = length
        self.count = count
        self.current = 0
        self.charset = charset or string.ascii_letters + string.digits

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.count:
            raise StopIteration
        self.current += 1
        return ''.join(random.choices(self.charset, k=self.length))


def main():
    password_generator = PasswordGenerator(10, 5)

    print("Using next() function:")
    print(next(password_generator))
    print(next(password_generator))

    print("\nUsing for loop:")
    for password in password_generator:
        print(password)


if __name__ == "__main__":
    main()
