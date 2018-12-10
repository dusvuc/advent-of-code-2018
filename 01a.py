def get_int(line):
    sign = line[0]
    val = int(line[1:])
    val = val if sign == "+" else -val
    return val


file = open("inputs\input01.txt", "r")
cnt = 0
for line in file:
    cnt += get_int(line)
print(cnt)