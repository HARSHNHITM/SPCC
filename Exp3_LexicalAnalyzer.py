def lexer(code):
    keywords = ["int", "float", "char"]
    operators = "+-*/="
    for token in code.replace(";", "").split():
        if token in keywords:
            print(f"{token} is a keyword")
        elif token in operators:
            print(f"{token} is an operator")
        elif token.isdigit():
            print(f"{token} is a number")
        elif token.isidentifier():
            print(f"{token} is an valid identifier")
        else:
            print(f"{token} is not valid")

lexer("int a = b + 1c;")