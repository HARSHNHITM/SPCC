# Simulate the three-address code
A = ["T=A+B", "X=T"]

# Extract operands and operator from the first expression
lhs = A[0][0]
op1 = A[0][2]
operator = A[0][3]
op2 = A[0][4]

print(f"MOV {op1}, R1")
print(f"MOV {op2}, R2")

# Show options to the user
print("THERE ARE TWO EXPRESSIONS:\n1. T = A OP B\n2. X = T")
print("CHOOSE THE OP VALUE FROM OPTIONS:")
print("1. +\n2. -\n3. *\n4. /")

op_choice = int(input("Enter your choice (1-4): "))

# Operator mapping
ops = {
    1: "ADD",
    2: "SUB",
    3: "MUL",
    4: "DIV"
}

if op_choice in ops:
    print(f"{ops[op_choice]} R1, R2")
else:
    print("Invalid operator selected")

print("MOV R1, X")
