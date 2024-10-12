#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 11:32:46 2024

Author: maxfroehner
"""

import os
import pandas as pd

# Function to read the questions from a file and separate by empty lines
def extract_questions(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        print(f"Skipping file {file_path} due to encoding issues.")
        return []

    # Split the content into questions based on double newlines
    questions = content.split('\n\n')
    
    # Strip whitespace and filter out empty questions
    questions = [q.strip() for q in questions if q.strip()]
    
    return questions

# Function to process all files in a directory and label with filename
def process_directory(directory_path):
    labeled_questions = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            questions = extract_questions(file_path)
            labeled_questions.extend([(filename, q) for q in questions])
    return labeled_questions

# Directories to process
directories = [
    '/Users/maxfroehner/Desktop/BMW_AI_answers',
    '/Users/maxfroehner/Desktop/BMW_questions_actual'
]

# Extract questions from each directory and label them
all_questions_dir1 = process_directory(directories[0])
all_questions_dir2 = process_directory(directories[1])

# Create DataFrames and save to an Excel file
df1 = pd.DataFrame(all_questions_dir1, columns=['Filename', 'Questions'])
df2 = pd.DataFrame(all_questions_dir2, columns=['Filename', 'Questions'])

output_file = '/Users/maxfroehner/Desktop/Extracted_Questions.xlsx'
with pd.ExcelWriter(output_file) as writer:
    df1.to_excel(writer, sheet_name='BMW_AI_answers', index=False)
    df2.to_excel(writer, sheet_name='BMW_questions_actual', index=False)

print(f"Questions extracted and saved to {output_file}")
