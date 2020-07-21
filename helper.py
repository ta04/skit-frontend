import libnum
import hashlib
import random


def generateN():
    n = libnum.generate_prime(24)
    return n


def generateV(n):
    v = random.randint(1, n)
    return v


def generateC(n):
    c = random.randint(1, n)
    return c


def calculateG(n):
    for x in range(1, n):
        rand = x
        exp = 1
        next = rand % n

        while (next != 1):
            next = (next*rand) % n
            exp = exp+1

        if (exp == n-1):
            return rand


def calculateX(password, n):
    x = int(hashlib.md5(password.encode()).hexdigest()[:8], 16) % n
    return x


def calculateY(g, x, n):
    y = pow(g, x, n)
    return y


def calculateT(g, v, n):
    t = pow(g, v, n)
    return t


def calculateR(v, c, x):
    r = (v - c * x)
    return r


def calculateResult(g, r, n, y, c):
    result = (libnum.invmod(pow(g, -r, n), n) * pow(y, c, n)) % n
    return result
