# parser.py
def clean_line(line):
    # Remove comments and all types of whitespace/newlines
    content = line.split('//')[0]
    return "".join(content.split())

def get_instructions(filename):
    instructions = []
    with open(filename, 'r') as file:
        for line in file:
            cleaned = clean_line(line)
            if cleaned:
                instructions.append(cleaned)
    return instructions