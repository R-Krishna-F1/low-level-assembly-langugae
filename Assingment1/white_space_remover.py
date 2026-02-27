import os

def preprocess_asm(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile:
                # Remove comments
                content = line.split('//')[0]
                # Remove all whitespace
                clean_content = "".join(content.split())
                
                if clean_content:
                    outfile.write(clean_content + "\n")
        print(f"Success: Cleaned {input_filename} and saved to {output_filename}")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    # Look for any file in the current folder ending with .asm
    asm_files = [f for f in os.listdir('.') if f.endswith('.asm') and f != 'out.asm']

    if not asm_files:
        print("Error: No .asm files found in this folder!")
    else:
        # If multiple .asm files exist, it picks the first one found
        target_file = asm_files[0]
        print(f"Found assembly file: {target_file}")
        preprocess_asm(target_file, "out.asm")