print("Recursive Descent Parsing For the following grammar:")
print("E  -> T E'\nE' -> + T E' | ε\nT  -> F T'\nT' -> * F T' | ε\nF  -> (E) | i\n")

s = list(input("Enter the string to be checked: "))
i = 0

def match(a):
    global i
    if i >= len(s):
        return False
    if s[i] == a:
        i += 1
        return True
    return False

def F():
    global i
    if match('('):
        if E():
            if match(')'):
                return True
        return False
    elif match('i'):
        return True
    else:
        return False

def Tx():
    if match('*'):
        if F() and Tx():
            return True
        return False
    return True  # ε

def T():
    return F() and Tx()

def Ex():
    if match('+'):
        if T() and Ex():
            return True
        return False
    return True  # ε

def E():
    return T() and Ex()

# Run the parser
if E() and i == len(s):
    print("String is accepted")
else:
    print("String is not accepted")
