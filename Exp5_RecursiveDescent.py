expr = input("Enter string: ")
i = 0

def match(x):
    global i
    if i < len(expr) and expr[i] == x:
        i += 1
        return True
    return False

def F():
    return match('i') or (match('(') and E() and match(')'))

def Tx():
    return match('*') and F() and Tx() or True

def T():
    return F() and Tx()

def Ex():
    return match('+') and T() and Ex() or True

def E():
    return T() and Ex()

print("Accepted" if E() and i == len(expr) else "Rejected")