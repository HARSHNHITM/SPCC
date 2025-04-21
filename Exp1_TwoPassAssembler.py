import sys

Opcodes = [
    "CLA", "LAC", "SAC", "ADD", "SUB", "BRZ", "BRN", "BRP",
    "INP", "DSP", "MUL", "DIV", "STP", "DATA", "START", "END"
]
AssemblyOpcodes = {
    "CLA": "0000", "LAC": "0001", "SAC": "0010", "ADD": "0011",
    "SUB": "0100", "BRZ": "0101", "BRN": "0110", "BRP": "0111",
    "INP": "1000", "DSP": "1001", "MUL": "1010", "DIV": "1011",
    "STP": "1100"
}

SymbolTable = []
LiteralTable = []
Declarations = []
AssemblyCode = []
Variables = []
location_counter = 0
stop_found = False
end_found = False

def check_literal(x): return x.startswith("='")
def remove_commas(x): return x[:-1] if x.endswith(",") else x

# Read input
with open("Assembly Code Input.txt", "r") as f:
    lines = [line.strip() for line in f if not line.strip().startswith("//")]

if "START" not in lines:
    print("STARTError: 'START' statement missing.")
    sys.exit(0)

lines = lines[lines.index("START") + 1:]

# Pass 1: Symbol Table and Literals
for line in lines:
    if not line or line.startswith("//"): continue
    parts = list(map(remove_commas, line.split()))
    if len(parts) >= 3 and parts[1] == "DATA":
        if parts[0] in Variables:
            print(f"DefinationError: Variable '{parts[0]}' defined multiple times.")
            sys.exit(0)
        Variables.append(parts[0])
        Declarations.append((parts[0], parts[2]))
        SymbolTable.append([parts[0], location_counter, parts[2], "Variable"])
        location_counter += 1
        stop_found = True
        continue
    if parts[0] == "END":
        end_found = True
        continue
    if len(parts) >= 2 and parts[1] in Opcodes:
        SymbolTable.append([parts[0], location_counter, None, "Label"])
    elif parts[0] in Opcodes:
        if len(parts) == 2:
            opnd = parts[1]
            if check_literal(opnd):
                LiteralTable.append([opnd, -1])
            elif not opnd.startswith("REG") and not opnd.isdigit():
                if not any(x[0] == opnd for x in SymbolTable):
                    SymbolTable.append([opnd, None, None, "Variable"])
    location_counter += 1

# Assign literal addresses
for i, literal in enumerate(LiteralTable):
    LiteralTable[i][1] = location_counter
    location_counter += 1

# Pass 2: Machine Code Generation
location_counter = 0
with open("Assembly Code Input.txt", "r") as f:
    lines = [line.strip() for line in f if not line.strip().startswith("//")]
lines = lines[lines.index("START") + 1:]

for line in lines:
    if not line or line.startswith("//"): continue
    parts = list(map(remove_commas, line.split()))
    if parts[0] == "END" or (len(parts) >= 3 and parts[1] == "DATA"):
        continue
    code = ""
    label_offset = 0
    if len(parts) == 2 and parts[0] in AssemblyOpcodes:
        op = parts[0]
        operand = parts[1]
    elif len(parts) == 3:
        label_offset = 1
        op = parts[1]
        operand = parts[2]
    elif len(parts) == 1:
        op = parts[0]
        operand = "00"
    else:
        continue

    opcode = AssemblyOpcodes.get(op, "0000")
    if check_literal(operand):
        addr = next(x[1] for x in LiteralTable if x[0] == operand)
    elif operand.startswith("REG"):
        addr = operand[-1].zfill(2)
    elif operand.isdigit():
        addr = operand.zfill(2)
    else:
        addr = next((str(s[1]).zfill(2) for s in SymbolTable if s[0] == operand), "00")
    
    AssemblyCode.append(f"{str(location_counter).zfill(2)} {opcode} 00 00 {addr}")
    location_counter += 1

print("\n>>> Opcode Table <<<\n")
print("ASSEMBLY OPCODE OPCODE\n--------------------------")
for k, v in AssemblyOpcodes.items():
    print(f"{k:<20}{v}")
print("--------------------------")

print("\n>>> Literal Table <<<\n")
print("LITERAL     ADDRESS\n-------------------")
for lit in LiteralTable:
    print(f"{lit[0]:<12} {lit[1]}")
print("-------------------")

print("\n>>> Symbol Table <<<\n")
print("SYMBOL         ADDRESS     VALUE      TYPE\n----------------------------------------------")
for sym in SymbolTable:
    print(f"{sym[0]:<16}{str(sym[1]):<12}{str(sym[2]):<10}{sym[3]}")
print("----------------------------------------------")

print("\n>>> Data Table <<<\n")
print("VARIABLES     VALUE\n-------------------")
for var, val in Declarations:
    print(f"{var:<14}{val}")
print("-------------------")

print("\n>>> MACHINE CODE <<<\n")
for mc in AssemblyCode:
    print(mc)