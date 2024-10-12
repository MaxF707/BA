import os
import re

def extract_middle_section(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_presentation_pattern = re.compile(r"^\s*Presentation\s*$", re.IGNORECASE)
    end_definitions_pattern = re.compile(r"^\s*Definitions\s*$", re.IGNORECASE)

    middle_section = []
    in_presentation = False

    for line in lines:
        if start_presentation_pattern.match(line):
            in_presentation = True
            continue

        if end_definitions_pattern.match(line):
            in_presentation = False

        if in_presentation:
            middle_section.append(line)

    return middle_section

def process_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, f"processed_{filename}")

            middle_section = extract_middle_section(input_file_path)

            with open(output_file_path, 'w') as output_file:
                output_file.writelines(middle_section)

# Paths
input_directory = '/Users/maxfroehner/Desktop/BMW_transcripts'
output_directory = '/Users/maxfroehner/Desktop/BMW_transcripts_LDA'

# Process files
process_files(input_directory, output_directory)
