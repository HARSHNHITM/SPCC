table = {
    ('E', 'i'): ['T', 'E''],
    ('E'', '+'): ['+', 'T', 'E''],
    ('E'', ')'): [],
    ('T', 'i'): ['F', 'T''],
    ('T'', '+'): [],
    ('F', 'i'): ['i'],
}

def parse(inp):
    stack = ['$', 'E']
    i = 0
    while stack:
        top = stack.pop()
        if top == '$': break
        curr = inp[i] if i < len(inp) else '$'
        if top == curr:
            i += 1
        elif (top, curr) in table:
            stack += reversed(table[(top, curr)])
        else:
            print("Rejected")
            return
    print("Accepted")

parse("i+i")