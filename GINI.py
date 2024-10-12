#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 11:33:58 2024

@author: maxfroehner
"""

import os
import numpy as np
from openpyxl import Workbook

def read_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def calculate_word_frequencies(text):
    words = text.split()
    frequency_dict = {}
    for word in words:
        word = word.lower()
        if word in frequency_dict:
            frequency_dict[word] += 1
        else:
            frequency_dict[word] = 1
    return np.array(list(frequency_dict.values()))

def gini_coefficient(array):
    sorted_array = np.sort(array)
    n = len(array)
    cumulative_sum = np.cumsum(sorted_array)
    relative_cumulative_sum = cumulative_sum / cumulative_sum[-1]
    index = np.arange(1, n + 1)
    return (n + 1 - 2 * np.sum(relative_cumulative_sum) / n) / n

def process_files_in_directory(directory_path, output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "Gini Scores"
    ws.append(["Filename", "Gini Index"])

    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            text = read_file(file_path)
            frequencies = calculate_word_frequencies(text)
            gini_index = gini_coefficient(frequencies)
            ws.append([filename, gini_index])
    
    wb.save(output_file)
    print(f"Gini scores saved to {output_file}")

# Example usage
directory_path = '/Users/maxfroehner/Desktop/BMW_transcripts_LDA'
output_file = 'BMW_transcripts_Gini_scores.xlsx'
process_files_in_directory(directory_path, output_file)
