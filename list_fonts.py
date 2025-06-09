import os
from pathlib import Path

def list_fonts(directory, output_file):
    # Convert directory to Path object for easier handling
    directory = Path(directory)
    
    # Initialize list to store font file paths
    font_files = []
    
    # Walk through directory
    for root, dirs, files in os.walk(directory):
        # Skip directories named 'tl'
        if 'tl' in dirs:
            dirs.remove('tl')
        
        # Check each file in current directory
        for file in files:
            if file.lower().endswith(('.otf', '.ttf')):
                # Get relative path from input directory
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                font_files.append(relative_path)
    
    # Write results to output file in the specified format
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("define game_fonts = [\n")
        for font in sorted(font_files):
            f.write(f'    "{font}",\n')
        f.write("]\n")
    
    print(f"Found {len(font_files)} font files. Results saved to {output_file}")

if __name__ == "__main__":
    # Get directory path from user
    user_dir = input("Enter the directory path to scan for fonts: ").strip()
    
    # Validate directory exists
    if not os.path.isdir(user_dir):
        print("Error: Invalid directory path")
    else:
        # Set output file path to script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, "font_list.txt")
        list_fonts(user_dir, output_path)