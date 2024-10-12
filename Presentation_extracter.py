#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 00:04:27 2024

@author: maxfroehner
"""

import os
import re

def extract_management_presentation(transcript_text):
    # Define the end pattern for the management presentation section
    end_pattern = r"(Questions and Answers)"
    
    # Search for the end position
    end_match = re.search(end_pattern, transcript_text, re.IGNORECASE)
    
    # Extract from the start of the document to the end pattern or the end of the document
    end_pos = end_match.start() if end_match else len(transcript_text)
    
    management_presentation = transcript_text[:end_pos].strip()
    return management_presentation

def process_transcripts(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each transcript in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            with open(input_path, 'r', encoding='utf-8') as file:
                transcript_text = file.read()
            
            management_presentation = extract_management_presentation(transcript_text)
            output_filename = f"presentation_{filename}"
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(management_presentation)
            print(f"Processed {filename}")

# Example usage:
input_directory = "/Users/maxfroehner/Desktop/BMW_transcripts"
output_directory = "/Users/maxfroehner/Desktop/BMW_presentations"
process_transcripts(input_directory, output_directory)
