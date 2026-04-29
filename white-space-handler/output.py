import os

def process_details():
    # Look for any .txt file in the folder
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt') and f != 'my details']

    if not txt_files:
        print("Error: No .txt files found in this folder!")
        return

    target_file = txt_files[0]
    print(f"Found details file: {target_file}")

    try:
        with open(target_file, 'r') as infile:
            content = infile.read()
        
        with open("my details", "w") as outfile:
            outfile.write(content)
            
        print(f"Success: Content from {target_file} copied to 'my details'.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_details()