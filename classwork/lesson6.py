import sys
import functools

def p(*args, sep = ' ', end = '/n'):
    for x in args:
        sys.stdout.write(str(x))
        sys.stdout.write(sep)
    sys.stdout.write(end)

p('hello', 'hi', True, 24, sep = ':', end = 'END!')
print()

x = 5
 
def add():
    x = 3
    x = x + 5
    print(x)
 
add()
print(x)
print()

l = [1, 2, 3]

m = map(str, l)

for x in m:
    print(x)

print()

def swap(a, b):
    a, b = b, a
 
a = 4
b = 3
swap(a, b)
print(a - b)

l = [1, 2, 3, 4, -5, 6]

def positive(n):
    if n > 0:
        return n

m = list(map(positive, l))
m = list(filter(positive, l))
m = list(filter(lambda n : n > 0, l))
print(m)
print()

def f(x):
    return x**2
 
g = f
print(f(3), g(5))

print()

def comparator(pair):
    return pair[0] + pair[1]
 
pairs = [(5, 4), (3, 2), (1, 7), (8, 2)]
pairs.sort(key=comparator, reverse=True)
print(pairs)

words = ['this', 'is', 'a', 'test', 'of', 'sorting']
words.sort(key=len)
print(words)