def parse(input_str):
    stack = ['$', 'S']
    i = 0
    while stack[-1] != '$':
        top = stack.pop()
        curr = input_str[i] if i < len(input_str) else '$'
        if top == curr:
            i += 1
        elif top == 'S' and curr == 'a':
            stack += ['B', 'S']
        elif top == 'S' and curr == 'b':
            continue
        elif top == 'B' and curr == 'b':
            stack.append('b')
        else:
            print("Rejected")
            return
    print("Accepted")

parse("ab")