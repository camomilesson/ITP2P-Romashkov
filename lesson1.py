n = int(input())

# Error handling as per Vladimir's request
if n < 1:
    raise ValueError('Give me a normal number, Vladimir!')

# Triangle
print('Triangle')
for i in range(n):
    line = '*' * (i + 1)
    print(line)
print()

# Triangle with extra spaces
print('Triangle with extra spaces')
for i in range(n):
    line = '* ' * (i + 1)
    print(line)
print()

# Flipped up-side-down triangle
print('Flipped up-side-down triangle')
for i in range(n):
    line = '* ' * (n - i)
    print(line)
print()

# Turned triangle
print('Turned triangle')
for i in range(n):
    line = '  ' * (n - i - 1) + '* ' * (i + 1)
    print(line)
print()

# Christmas tree
print('Christmas tree')
for i in range(n):
    line = ' ' * (n - i - 1) + '* ' * (i + 1)
    print(line)
print()

# Empty Christmas tree
print('Empty Christmas tree')
print(' ' * (n - 1) + '*')
for i in range(1, n - 1):
    line = ' ' * (n - i - 1) + '* ' + ' ' * (2 * (i -1)) + '*'
    print(line)
print('* ' * n)
print()

# Alternating numbers
print('Alternating numbers')
for i in range(n):
    line = f'{i + 1} ' * (i + 1)
    print(line)
print()

# 🌶️ Numbered triangle
print('🌶️ Numbered triangle')
number = 1
for row in range(1, n + 1):
    for col in range(1, row + 1):
        print(number, end = ' ')
        number += 1
    print()
print()

# 🌶️🌶️ Numbered Christmas tree
print('🌶️🌶️ Numbered Christmas tree')
number = 1
for row in range(1, n + 1):
    padding = ' ' * (n - row)
    print(padding, end = '')
    for col in range(1, row + 1):
        print(number, end = ' ')
        number += 1
    print()
print()