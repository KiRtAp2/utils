import re

in_ = input()
n = int(input())

cmp_with = r"^"

for c in in_:
    if c=='?':
        cmp_with += '.'
    elif c=='*':
        cmp_with += '.*'
    else:
        cmp_with += c

cmp_with += '$'
m = 0

for i in range(n):
    s = input()
    if re.match(cmp_with, s):
        m += 1

print(m)
