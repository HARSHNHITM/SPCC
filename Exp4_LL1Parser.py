def parse(input_str):
    stack = ['$', 'S']
    i = 0
    input_str += '$'  # End marker
    max_steps = 100  # safety cap

    steps = 0
    while stack and steps < max_steps:
        top = stack.pop()
        curr = input_str[i] if i < len(input_str) else '$'

        # Debugging output
        print(f"STACK: {stack} | CURRENT: {curr} | TOP: {top}")

        if top == curr:
            i += 1
        elif top == 'S':
            if curr == 'a':
                stack += ['B', 'S']  # S → a S B
            elif curr in ['b', '$']:
                continue  # ε
            else:
                print("Rejected")
                return
        elif top == 'B':
            if curr == 'b':
                stack.append('b')  # B → b
            else:
                print("Rejected")
                return
        elif top == '$':
            if curr == '$':
                print("Accepted")
                return
            else:
                print("Rejected")
                return
        else:
            print("Rejected")
            return
        steps += 1

    print("Rejected (safety stop or invalid input)")

# ✅ Test Case
parse("aabbb")
