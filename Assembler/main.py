# main.py
import tables
import parser

def assemble(input_file):
    raw_lines = parser.get_instructions(input_file)
    symbol_table = tables.SYMBOLS.copy()
    
    # PASS 1: Labels
    temp_stream = []
    rom_addr = 0
    for line in raw_lines:
        if line.startswith("(") and line.endswith(")"):
            symbol_table[line[1:-1]] = rom_addr
        else:
            temp_stream.append(line)
            rom_addr += 1

    # PASS 2: Variables & Symbols (Creates out.asm)
    resolved_lines = []
    next_var_addr = 16
    for line in temp_stream:
        if line.startswith("@"):
            val = line[1:]
            if not val.isdigit():
                if val not in symbol_table:
                    symbol_table[val] = next_var_addr
                    next_var_addr += 1
                val = symbol_table[val]
            resolved_lines.append(f"@{val}")
        else:
            resolved_lines.append(line)

    with open("out.asm", "w") as f:
        f.write("\n".join(resolved_lines))
    print("Generated 1: out.asm")

    # PASS 3: Binary
    binary_codes = []
    for line in resolved_lines:
        if line.startswith("@"):
            val = int(line[1:])
            binary_codes.append(bin(val)[2:].zfill(16))
        else:
            dest, jump = "", ""
            curr = line
            if "=" in curr:
                dest, curr = curr.split("=")
            if ";" in curr:
                curr, jump = curr.split(";")
            
            # Scrub any remaining whitespace to prevent KeyErrors
            comp_key = curr.strip()
            dest_key = dest.strip()
            jump_key = jump.strip()
            
            binary_codes.append(f"111{tables.COMP_TABLE[comp_key]}{tables.DEST_TABLE[dest_key]}{tables.JUMP_TABLE[jump_key]}")

    with open("program.hack", "w") as f:
        f.write("\n".join(binary_codes))
    print("Generated 2: program.hack")

if __name__ == "__main__":
    assemble("input.asm")