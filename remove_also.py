#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 21:58:38 2024

@author: maxfroehner
"""

import os

# Path to the directory containing the documents
directory_path = '/Users/maxfroehner/Desktop/MB_preprocessed'

# Function to remove the word "also" from a text
def remove_word(text, word):
    # Replace the word "also" with an empty string
    return text.replace(word, '')

# Process each document in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        # Read the document
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as file:
            text = file.read()
        
        # Remove the word "also"
        cleaned_text = remove_word(text, 'also')
        
        # Save the cleaned text back to the file
        with open(file_path, 'w') as file:
            file.write(cleaned_text)

print("The word 'also' has been removed from all documents.")
