def fibonacci(x, y):
    if y > 100000000:
        return

    print(x)
    fibonacci(y, x + y)

fibonacci(0, 1)


def count_to_100(x):
    if x > 100:
        return
    print(x)
    count_to_100(x + 1)

count_to_100(0)

def summa(x):
    if x == 1:
        return 1
    else:
        return x + summa(x - 1)

print(summa(10))