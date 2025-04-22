import sys
import re

def clean_token(token):
    return token.strip().rstrip(',')

def is_literal(token):
    return token.startswith("='")

def is_valid_symbol(token, prev_token, opcodes, symbol_table):
    return (token != "CLA" and prev_token not in ["BRP", "BRN", "BRZ"] and
            not is_literal(token) and not token.startswith("REG") and
            not token.isdigit() and [token, None, None, "Variable"] not in symbol_table)

def is_valid_label(token, opcodes, symbol_table):
    return token not in [s[0] for s in symbol_table] and token not in opcodes

opcodes = ["CLA", "LAC", "SAC", "ADD", "SUB", "BRZ", "BRN", "BRP", "INP",
           "DSP", "MUL", "DIV", "STP", "DATA", "START"]
assembly_opcodes = {"CLA": "0000", "LAC": "0001", "SAC": "0010", "ADD": "0011",
                    "SUB": "0100", "BRZ": "0101", "BRN": "0110", "BRP": "0111",
                    "INP": "1000", "DSP": "1001", "MUL": "1010", "DIV": "1011",
                    "STP": "1100"}

def assembler_pass_one(input_file):
    symbol_table = []
    literal_table = []
    variables = []
    declarations = []
    location_counter = 0
    stop_found = False
    end_found = False

    try:
        with open(input_file, "r") as f:
            # Read all lines and filter out comments and empty lines
            lines = []
            for line in f:
                # Remove comments and leading/trailing whitespace
                cleaned_line = line.split("//")[0].strip()
                # Skip empty lines and comment-only lines
                if cleaned_line and not cleaned_line.startswith("//"):
                    # Split by whitespace and filter out empty tokens
                    tokens = [t.strip() for t in cleaned_line.split()]
                    if tokens:  # Only add non-empty token lists
                        lines.append(" ".join(tokens))

        if not lines:
            raise Exception("Input file is empty or contains only comments")
        if lines[0] != "START":
            raise Exception("START statement missing")
    except FileNotFoundError:
        raise Exception(f"Could not find input file: {input_file}")

    for line in lines[1:]:  # Skip START
        tokens = list(map(clean_token, line.split()))
        if not tokens:
            continue

        if tokens[0] == "END":
            end_found = True
            break

        if len(tokens) >= 3 and tokens[0] in opcodes:
            raise Exception(f"Too many operands for {tokens[0]}")
        elif len(tokens) == 1 and tokens[0] in ["LAC", "SAC", "ADD", "SUB", "BRZ", "BRN", "BRP", "INP", "DSP", "MUL", "DIV"]:
            raise Exception(f"Missing operand for {tokens[0]}")
        elif len(tokens) == 2 and tokens[1] in ["LAC", "SAC", "ADD", "SUB", "BRZ", "BRN", "BRP", "INP", "DSP", "MUL", "DIV"]:
            raise Exception(f"Missing operand for {tokens[1]}")

        if not stop_found:
            for tok in tokens:
                if is_literal(tok):
                    literal_table.append([tok, location_counter])

            if len(tokens) >= 2 and is_valid_label(tokens[0], opcodes, symbol_table):
                symbol_table.append([tokens[0], location_counter, None, "Label"])

            if len(tokens) > 0 and tokens[-1] not in opcodes and is_valid_symbol(tokens[-1], tokens[-2] if len(tokens) > 1 else '', opcodes, symbol_table):
                symbol_table.append([tokens[-1], None, None, "Variable"])

        elif tokens[0] != "STP":
            if tokens[0] not in variables:
                variables.append(tokens[0])
                declarations.append((tokens[0], tokens[2]))
            else:
                raise Exception(f"Variable {tokens[0]} already defined")

            try:
                sym_idx = next(i for i, s in enumerate(symbol_table) if s[0] == tokens[0])
                symbol_table[sym_idx][1] = location_counter
                symbol_table[sym_idx][2] = tokens[2]
            except StopIteration:
                raise Exception(f"{tokens[0]} declared but not used")

        if tokens[0] == "STP":
            stop_found = True

        location_counter += 1

    if not end_found:
        raise Exception("END statement missing")

    for sym in symbol_table:
        if sym[1] is None and sym[3] == "Variable":
            raise Exception(f"Variable {sym[0]} undefined")

    return symbol_table, literal_table, declarations, assembly_opcodes

def assembler_pass_two(input_file, symbol_table, literal_table, assembly_opcodes, output_file="Assembly Code Input.txt"):
    assembly_code = []

    with open(input_file, "r") as f:
        lines = [line.split("//")[0].strip() for line in f if line.strip() and not line.strip().startswith("//")]

    with open(output_file, "w") as outfile:
        outfile.write("------\nMACHINE CODE\n--------\n\n")

        for line in lines:
            tokens = list(map(clean_token, line.split()))
            if not tokens:
                continue

            if tokens[0] == "START":
                continue

            if tokens[0] == "END" or (len(tokens) == 3 and tokens[1] == "DATA"):
                break

            code = ""  # Initialize code for each iteration

            if tokens[0] == "STP":
                code = f"00 {assembly_opcodes['STP']} 00 00 00"
            elif len(tokens) == 2 and tokens[1] == "CLA":
                try:
                    addr = next(s[1] for s in symbol_table if s[0] == tokens[0])
                    code = f"{str(addr).rjust(2, '0')} {assembly_opcodes['CLA']} 00 00 00"
                except StopIteration:
                    raise Exception(f"Symbol {tokens[0]} not found")
            elif tokens[0] != "START":
                if len(tokens) == 2:
                    code = f"00{assembly_opcodes.get(tokens[0], '')}"
                    operand = tokens[1]
                    try:
                        if is_literal(operand):
                            addr = next(l[1] for l in literal_table if l[0] == operand)
                            code += f"0000{str(addr).rjust(2, '0')}"
                        elif tokens[0] in ["BRP", "BRN", "BRZ"]:
                            addr = next(s[1] for s in symbol_table if s[0] == operand)
                            code += f"{str(addr).rjust(2, '0')}0000"
                        elif operand.startswith("REG"):
                            code += f"00{operand[-1].rjust(2, '0')}00"
                        else:
                            addr = next(s[1] for s in symbol_table if s[0] == operand)
                            code += f"0000{str(addr).rjust(2, '0')}"
                    except StopIteration:
                        raise Exception(f"Symbol or literal {operand} not found")
                elif len(tokens) == 3:
                    try:
                        code = next(str(s[1]).rjust(2, '0') + " " + assembly_opcodes.get(tokens[1], '') for s in symbol_table if s[0] == tokens[0])
                        operand = tokens[2]
                        if is_literal(operand):
                            addr = next(l[1] for l in literal_table if l[0] == operand)
                            code += f"0000{str(addr).rjust(2, '0')}"
                        elif tokens[1] in ["BRP", "BRN", "BRZ"]:
                            addr = next(s[1] for s in symbol_table if s[0] == operand)
                            code += f"{str(addr).rjust(2, '0')}0000"
                        elif operand.startswith("REG"):
                            code += f"00{operand[-1].rjust(2, '0')}00"
                        else:
                            addr = next(s[1] for s in symbol_table if s[0] == operand)
                            code += f"0000{str(addr).rjust(2, '0')}"
                    except StopIteration:
                        raise Exception(f"Symbol {tokens[0]} or {operand} not found")

            if code:  # Only append and write if code was generated
                assembly_code.append(code)
                outfile.write(str(code) + "\n")

    return assembly_code

if __name__ == "__main__":
    try:
        symbol_table, literal_table, declarations, assembly_opcodes = assembler_pass_one("Assembly Code Input.txt")

        print(">>> Opcode Table <<<\nASSEMBLY OPCODE OPCODE\n--------------------")
        for key, value in assembly_opcodes.items():
            print(f"{key.ljust(20)}{value.ljust(6)}")
        print("--------------------\n")

        print(">>> Literal Table <<<\nLITERAL ADDRESS\n-------------------")
        for lit in literal_table:
            print(f"{lit[0].ljust(12)}{str(lit[1]).ljust(7)}")
        print("-------------------\n")

        print(">>> Symbol Table <<<\nSYMBOL ADDRESS  VALUE     TYPE\n-----------------------")
        for sym in symbol_table:
            print(f"{sym[0].ljust(16)}{str(sym[1]).ljust(12)}{str(sym[2]).ljust(10)}{sym[3].ljust(10)}")
        print("-----------------------\n")

        print(">>> Data Table <<<\nVARIABLES       VALUE\n-------------------")
        for dec in declarations:
            print(f"{dec[0].ljust(14)}{str(dec[1]).ljust(10)}")
        print("-------------------\n")

        assembler_pass_two("Assembly Code Input.txt", symbol_table, literal_table, assembly_opcodes)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)