#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:19:52 2024

@author: maxfroehner
"""

import os
import re
from openpyxl import Workbook  # Import openpyxl

def gunning_fog_index(text):
    sentences = re.split(r'[.!?]', text)
    sentences = list(filter(None, sentences))
    num_sentences = len(sentences)
    
    words = re.findall(r'\w+', text)
    num_words = len(words)
    
    complex_words = [word for word in words if len(re.findall(r'[aeiouyAEIOUY]', word)) >= 3]
    num_complex_words = len(complex_words)
    
    avg_sentence_length = num_words / num_sentences
    complex_word_percentage = (num_complex_words / num_words) * 100
    
    fog_index = 0.4 * (avg_sentence_length + complex_word_percentage)
    return fog_index

# Input and output directories
input_directory = "/Users/maxfroehner/Desktop/MB_transcripts_LDA"
output_directory = "/Users/maxfroehner/Desktop/MB_transcripts_Gunning"
output_file = os.path.join(output_directory, "Gunning_Fog_Results.xlsx")

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Create a new workbook and select the active worksheet
wb = Workbook()
ws = wb.active
ws.title = "Gunning Fog Index"

# Write header
ws.append(["Filename", "Gunning Fog Index"])

# Iterate through each file and calculate the Gunning Fog Index
for filename in os.listdir(input_directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            index = gunning_fog_index(text)
            ws.append([filename, index])
            print(f"Processed {filename}: Gunning Fog Index = {index:.2f}")

# Save the workbook
wb.save(output_file)

print(f"All results saved to {output_file}")
