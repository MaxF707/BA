#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 16:30:59 2024

@author: maxfroehner
"""

import pandas as pd

# Read the Excel file
df = pd.read_excel('/Users/maxfroehner/Desktop/BMW_EPS/BMW_EPS_clean.xlsx')

# Loop through each row and write to a text file
for index, row in df.iterrows():
    # Use the content of the first column for the file name
    first_column_content = row[df.columns[0]]
    file_name = f'EPS_vs_Estimate_20{first_column_content}.txt'
    with open(file_name, 'w') as file:
        for col in df.columns:
            file.write(f'{col}: {row[col]}\n')

print("Files created successfully.")
