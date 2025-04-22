import re

def process_macros(input_file):
    mnt = []  # Macro Name Table
    ala = []  # Argument List Array
    mdt = []  # Macro Definition Table
    pass1_output = []

    with open(input_file, 'r') as infile:
        lines = [line.strip() for line in infile]

    macro_mode = False
    macro_name = None
    macro_args = []
    mdt_index = 1

    for line in lines:
        if line.upper() == 'MACRO':
            macro_mode = True
            continue

        if macro_mode:
            parts = re.split(r'\s+', line, maxsplit=1)
            if len(parts) > 1:
                name, args_str = parts[0], parts[1]
            else:
                name = parts[0]
                args_str = ""

            if macro_name is None:
                macro_name = name
                macro_args = [arg.split('=')[0] for arg in args_str.split(',') if arg]
                mnt.append((macro_name, mdt_index))
                for arg in macro_args:
                    ala.append(arg)
            else:
                for i, arg in enumerate(macro_args):
                    line = re.sub(rf'&{arg}\b', f'#{i}', line)
                mdt.append(line)
                mdt_index += 1

            if line.upper() == 'MEND':
                macro_mode = False
                macro_name = None
                pass
        else:
            pass1_output.append(line)

    return mnt, ala, mdt, pass1_output

def expand_macros(pass1_output, mnt, mdt):
    pass2_output = []
    ala_pass2 = []

    for line in pass1_output:
        parts = re.split(r'\s+', line, maxsplit=1)
        macro_name = parts[0]
        args_str = parts[1] if len(parts) > 1 else ""

        macro_entry = next((entry for entry in mnt if entry[0] == macro_name), None)
        if macro_entry:
            mdt_start_index = macro_entry[1] - 1
            macro_args_pass2 = args_str.split(',') if args_str else []
            ala_pass2.extend(macro_args_pass2)
            for i, expanded_line in enumerate(mdt[mdt_start_index: ]):
                if expanded_line.upper() == 'MEND':
                    break
                for j, arg in enumerate(macro_args_pass2):
                    expanded_line = re.sub(rf'#{j}\b', arg, expanded_line)
                pass2_output.append(expanded_line)
        else:
            pass2_output.append(line)

    return pass2_output, ala_pass2

def display_table(table):
    for row in table:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    mnt, ala, mdt, pass1_output = process_macros("input.txt")
    pass2_output, ala_pass2 = expand_macros(pass1_output, mnt, mdt)

    print("Macro Name Table (MNT)")
    display_table(mnt)

    print("\nArgument List Array (ALA) for Pass 1")
    print(ala)

    print("\nMacro Definition Table (MDT)")
    for line in mdt:
        print(line)

    print("\nArgument List Array (ALA) for Pass 2")
    print(ala_pass2)

    with open("pass1_output.txt", "w") as outfile:
        outfile.write('\n'.join(pass1_output))

    with open("pass2_output.txt", "w") as outfile:
        outfile.write('\n'.join(pass2_output))