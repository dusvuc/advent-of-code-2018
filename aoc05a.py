

def react_polymer(line):
    should_iterate = True
    while should_iterate:
        should_iterate = False
        cnt = 0
        line_length = len(line)
        while not cnt >= line_length-1:
            if line[cnt].lower() == line[cnt+1].lower() and line[cnt] != line[cnt+1]:
                should_iterate = True
                line = line[:cnt] + line[cnt+2:]
                line_length -= 2
            else:
                cnt += 1
    return line


if __name__ == '__main__':
    line = open("inputs/input05.txt").readlines()[0].strip()
    res = react_polymer(line)
    print(len(res))