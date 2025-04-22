assembly = [
    "START", "LAC A", "ADD B", "SAC C", "STP",
    "A DATA 5", "B DATA 10", "C DATA 0", "END"
]

symbol_table = {}
machine_code = []
lc = 0

# Pass 1
for line in assembly:
    parts = line.split()
    if "DATA" in line:
        symbol_table[parts[0]] = {"addr": lc, "value": parts[2]}
    elif parts[0] not in ["START", "END"]:
        lc += 1

# Pass 2
opcodes = {"LAC": "0001", "ADD": "0011", "SAC": "0010", "STP": "1100"}
for line in assembly:
    parts = line.split()
    if parts[0] in opcodes:
        mc = f"{opcodes[parts[0]]} {symbol_table[parts[1]]['addr']}"
        machine_code.append(mc)
    elif parts[0] in symbol_table:
        continue
    elif parts[0] == "STP":
        machine_code.append(f"{opcodes['STP']} 00")

print("Machine Code:")
for code in machine_code:
    print(code)
