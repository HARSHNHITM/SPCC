# Predictive Parsing Table for LL(1) Grammar
table = {
    ('E', 'i'): ['T', "E'"],
    ('E', '('): ['T', "E'"],

    ("E'", '+'): ['+', 'T', "E'"],
    ("E'", ')'): [],  # ε
    ("E'", '$'): [],  # ε

    ('T', 'i'): ['F', "T'"],
    ('T', '('): ['F', "T'"],

    ("T'", '+'): [],  # ε
    ("T'", '*'): ['*', 'F', "T'"],
    ("T'", ')'): [],  # ε
    ("T'", '$'): [],  # ε

    ('F', 'i'): ['i'],
    ('F', '('): ['(', 'E', ')'],
}

def predictive_parse(input_string):
    input_string += '$'
    stack = ['$', 'E']
    i = 0

    print("\nStack\t\tInput\t\tAction")
    print("-------------------------------------------")

    while stack:
        top = stack.pop()
        current = input_string[i]

        print(f"{''.join(stack):<10}\t{input_string[i:]}\t", end="")

        if top == current:
            print(f"Match {current}")
            i += 1
            if current == '$':
                print("SUCCESS: Input string is accepted.")
                return
        elif (top, current) in table:
            production = table[(top, current)]
            print(f"{top} → {' '.join(production) if production else 'ε'}")
            for symbol in reversed(production):
                stack.append(symbol)
        else:
            print(f"ERROR: No rule for ({top}, {current})")
            return

    print("Rejected")

# 🔽 Test it
user_input = input("Enter the input string (like i+i*i): ")
predictive_parse(user_input)
