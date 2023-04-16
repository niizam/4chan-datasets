import os
import argparse

# Set up command-line argument parser
parser = argparse.ArgumentParser(description='Merge text files in a directory.')
parser.add_argument('-d', '--directory', required=True, help='Path to the input directory containing .txt files')
parser.add_argument('-o', '--output', required=True, help='Path to the output file')

# Parse the command-line arguments
args = parser.parse_args()

dir_path = args.directory

# Get a list of all .txt files in the directory
txt_files = [f for f in os.listdir(dir_path) if f.endswith('.txt')]

# Open a new file for writing
with open(args.output, 'w') as outfile:
    # Loop through each file and append its contents to the merged file
    for file in txt_files:
        with open(os.path.join(dir_path, file), 'r') as infile:
            outfile.write(infile.read())