#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:26:35 2024

@author: maxfroehner
"""

import pandas as pd
import os

# Initialize a list to store the results
results = []

# Directory containing .txt files
directory = "/Users/maxfroehner/Desktop/BMW_transcripts_LDA_output"

# Iterate through each output file
for filename in os.listdir(directory):
    if filename.endswith("_fog_index.txt"):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
            results.append(line.split(": "))

# Convert the results to a DataFrame
df = pd.DataFrame(results, columns=["File Name", "Gunning Fog Index"])

# Save to a single Excel file
output_path = "/Users/maxfroehner/Desktop/Gunning_Fog_Index_Results.xlsx"
df.to_excel(output_path, index=False)

# Optionally, save to a CSV file
#output_csv_path = "/Users/maxfroehner/Desktop/Gunning_Fog_Index_Results.csv"
#df.to_csv(output_csv_path, index=False)

print(f"Results saved to {output_path}")
