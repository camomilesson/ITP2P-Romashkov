print('\n'.join(['*' * int(n) for n in input().split()]))


n = int(input())
m = [list(map(int, input().split())) for _ in range(n)]

for i in range(n):
    for j in range(n):
        if i == j and i <= n // 2:
            temp = m[i][j]
            m[i][j] = m[n - j - 1][n - i - 1]
            m[n - j - 1][n - i - 1] = temp
        elif i == n - j and i <= n // 2:
            temp = m[i][j]
            m[i][j] = m[j][i]
            m[j][i] = temp

for line in m:
    for element in line:
        print(element, '', end = '')
    print()

    