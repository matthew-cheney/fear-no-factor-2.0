import math

def getFactors(n):
    print('getting factors for ', n)
    if n == -1:
        return {()}
    if n == 1:
        return {(1,1)}
    pairs = set()
    for i in range(1, (int(math.sqrt(n)) + 1)):
        if n % i == 0:
            factors = (i, n // i)
            pairs.add((min(factors), max(factors)))
    return pairs

# assert getFactors(10) == {(1, 10), (2, 5)}
# assert getFactors(17) == {(1, 17)}