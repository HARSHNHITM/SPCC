
def parse(input_str):
    stack = ['$', 'S']
    i = 0
    print("Parsing:", input_str)
    while stack[-1] != '$':
        top = stack.pop()
        curr = input_str[i] if i < len(input_str) else '$'
        print(f"Stack: {stack}, Current: {curr}, Top: {top}")
        if top == curr:
            i += 1
        elif top == 'S' and curr == 'a':
            stack.extend(['B', 'a'])
        elif top == 'S' and curr == 'b':
            stack.append('b')
        elif top == 'B' and curr == 'b':
            stack.append('b')
        else:
            print("Rejected")
            return
    if i == len(input_str):
        print("Accepted")
    else:
        print("Rejected")

# Get input from user
input_str = input("Enter string to parse: ")
parse(input_str)
