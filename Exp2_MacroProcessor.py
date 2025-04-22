import re
import sys

def macro_pass1(input_filename="macro_input.txt", pass1_output_filename="pass1_output.txt"):
    mnt = []  # Macro Name Table: List of [index, macro_name, mdt_index]
    ala = []  # Argument List Array: List of [index, argument_name]
    mdt = []  # Macro Definition Table: List of macro definition lines
    mntc = 1
    mdtc = 1
    alac = 0

    try:
        with open(input_filename, 'r') as infile, open(pass1_output_filename, 'w') as outfile:
            reading_macro = False
            macro_name = None
            macro_args = []

            for line_number, line in enumerate(infile, start=1):
                line = line.strip()
                tokens = line.split()

                try:
                    if tokens and tokens[0].upper() == "MACRO":
                        reading_macro = True
                        if len(tokens) > 1:
                            macro_name_and_args = tokens[1].split(None, 1)
                            macro_name = macro_name_and_args[0]
                            args_str = macro_name_and_args[1] if len(macro_name_and_args) > 1 else ""
                            args = [arg.split('=')[0] for arg in args_str.split(',') if args_str]
                        else:
                            macro_name = ""
                            args = []

                        mnt.append([mntc, macro_name, mdtc])
                        mntc += 1

                        for arg in args:
                            ala.append([alac, arg])  # Store argument name directly
                            alac += 1
                        mdt.append(line)
                        mdtc += 1

                    elif reading_macro:
                        if tokens and tokens[0].upper() == "MEND":
                            reading_macro = False
                            mdt.append(line)
                            mdtc += 1
                        else:
                            for i, arg in enumerate(macro_args):
                                line = re.sub(r'&' + arg, '#' + str(i), line)
                            mdt.append(line)
                            mdtc += 1
                    else:
                        outfile.write(line + '\n')

                except Exception as e:
                    print(f"Error processing line {line_number}: {line}")
                    print(f"  {e}")
                    return

        display_tables(mnt, ala, mdt)  # Ensure ALA is passed here

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An unrecoverable error occurred during Pass 1: {e}")


def macro_pass2(pass1_output_filename="pass1_output.txt", pass2_output_filename="pass2_output.txt"):
    mnt = []  # Macro Name Table: List of [index, macro_name, mdt_index, arg_count]
    mdt = []  # Macro Definition Table: List of macro definition lines
    mntc = 1
    mdtc = 1

    try:
        with open("macro_input.txt", 'r') as infile:  # Re-read the original input
            reading_macro = False
            macro_name = None
            macro_args = []

            for line_number, line in enumerate(infile, start=1):
                line = line.strip()
                tokens = line.split()

                if tokens and tokens[0].upper() == "MACRO":
                    reading_macro = True
                    if len(tokens) > 1:
                        macro_name_and_args = tokens[1].split(None, 1)
                        macro_name = macro_name_and_args[0]
                        args_str = macro_name_and_args[1] if len(macro_name_and_args) > 1 else ""
                        macro_args = [arg.split('=')[0] for arg in args_str.split(',') if args_str]
                    else:
                        macro_name = ""
                        macro_args = []

                    mnt.append([mdtc, macro_name, mdtc, len(macro_args)])  # Store arg count
                    mdt.append(line)
                    mdtc += 1

                elif reading_macro:
                    if tokens and tokens[0].upper() == "MEND":
                        reading_macro = False
                        mdt.append(line)
                        mdtc += 1
                    else:
                        for i, arg in enumerate(macro_args):
                            line = re.sub(r'&' + arg, '#' + str(i), line)  # Local index
                        mdt.append(line)
                        mdtc += 1
                else:
                    pass
    except FileNotFoundError:
        print(f"Error: Input file 'macro_input.txt' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        with open(pass1_output_filename, 'r') as infile, open(pass2_output_filename, 'w') as outfile:
            for line in infile:
                line = line.strip()
                tokens = line.split()
                expanded = False

                if tokens:
                    for m in mnt:
                        if tokens[0] == m[1]:  # Macro call found
                            mdt_index = m[2]
                            arg_count = m[3]
                            actual_args = tokens[1].split(',') if len(tokens) > 1 else []
                            try:
                                expand_macro(mdt, mdt_index, arg_count, actual_args, outfile)
                                expanded = True
                                break
                            except Exception as e:
                                print(f"Error expanding macro '{m[1]}': {e}")
                if not expanded and tokens:
                    outfile.write(line + '\n')

    except FileNotFoundError:
        print(f"Error: Input file '{pass1_output_filename}' not found.")
    except Exception as e:
        print(f"An error occurred during Pass 2: {e}")


def expand_macro(mdt, mdt_index, arg_count, actual_args, outfile):
    for i in range(mdt_index + 1, len(mdt)):
        def_line = mdt[i]
        if def_line.upper().strip() == "MEND":
            break
        expanded_line = def_line
        try:
            for j in range(len(actual_args)):
                expanded_line = re.sub(r'#' + str(j), actual_args[j], expanded_line)  # Local index
            outfile.write(expanded_line + '\n')
        except Exception as e:
            print(f"Error expanding line '{def_line}': {e}")


def display_tables(mnt, ala, mdt):
    print("\nMacro Name Table (MNT):")
    print("---------------------------")
    print("Index\tMacro Name\tMDT Index")
    print("---------------------------")
    for m in mnt:
        print(f"{m[0]}\t{m[1]}\t\t{m[2]}")

    print("\nArgument List Array (ALA):")
    print("---------------------------")
    print("Index\tArgument Name")
    print("---------------------------")
    for a in ala:
        print(f"{a[0]}\t{a[1]}")

    print("\nMacro Definition Table (MDT):")
    print("---------------------------")
    print("Index\tDefinition")
    print("---------------------------")
    for i, d in enumerate(mdt):
        print(f"{i + 1}\t{d}")
    print("\n")


if __name__ == "__main__":
    macro_pass1()
    macro_pass2()