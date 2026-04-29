import re
import os

def tokenize_jack_files():
    # --- STEP 1: Define our "Dictionaries" (Lists) of rules ---
    keywords = [
        'class', 'constructor', 'function', 'method', 'field', 'static', 
        'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 
        'this', 'let', 'do', 'if', 'else', 'while', 'return'
    ]
    
    symbols = [
        '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', 
        '&', '|', '<', '>', '=', '~'
    ]

    # --- STEP 2: Find and Loop through files ---
    current_folder = os.listdir('.') 
    
    for filename in current_folder:
        # FIX: Check if it ends in .jack AND is a file (not a folder)
        if filename.endswith(".jack") and os.path.isfile(filename):
            print(f"Tokenizing: {filename}...")
            
            with open(filename, 'r') as f:
                code = f.read()

            # --- STEP 3: Clean up (Remove comments) ---
            # Remove /* ... */ comments
            code = re.sub(r'/\*.*?\*/', ' ', code, flags=re.DOTALL)
            # Remove // comments
            code = re.sub(r'//.*?\n', '\n', code)

            # --- STEP 4: The "Sieve" (Find all tokens) ---
            # This regex catches: "Strings", Symbols, Numbers, and Words
            pattern = r'"[^"\n]*"|' + '|'.join(map(re.escape, symbols)) + r'|\d+|[\w_]+'
            tokens = re.findall(pattern, code)

            # --- STEP 5: Create and Write to the XML file ---
            output_name = filename.replace(".jack", ".xml")
            with open(output_name, 'w') as out:
                out.write("<tokens>\n")
                
                for t in tokens:
                    # Decide the type (Tag)
                    if t in keywords:
                        tag = "keyword"
                        val = t
                    elif t in symbols:
                        tag = "symbol"
                        # Escape special XML characters
                        val = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    elif t.isdigit():
                        tag = "integerConstant"
                        val = t
                    elif t.startswith('"'):
                        tag = "stringConstant"
                        val = t[1:-1] # Remove the quotes
                    else:
                        tag = "identifier"
                        val = t
                    
                    # Write the line
                    out.write(f"<{tag}> {val} </{tag}>\n")
                
                out.write("</tokens>\n")
            
            print(f"Finished! Created: {output_name}")

if __name__ == "__main__":
    tokenize_jack_files()