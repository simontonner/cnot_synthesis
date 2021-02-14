import time


def is_prime(n):
    if (n <= 1):
        return 'not a prime number'
    if (n <= 3):
        return 'prime number'

    if (n % 2 == 0 or n % 3 == 0):
        return 'not a prime number'

    i = 5
    while (i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0):
            return 'not a prime number'
        i = i + 6

    return 'prime number'


starttime = time.time()
for i in range(1, 10):
    time.sleep(2)
    print('{} is {} number'.format(i, is_prime(i)))
print()
print('Time taken = {} seconds'.format(time.time() - starttime))