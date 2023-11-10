import sys

lines = []

try:
    for line in sys.stdin:
        lines.append(line)
except:
    pass

print("Here's your output:")

for line in lines:
    print('\''+line.rstrip('\n')+'\\n\',')
