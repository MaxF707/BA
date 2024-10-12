import os
import glob
import pandas as pd
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from nltk.tokenize import word_tokenize
from openpyxl import Workbook

def safe_sheet_name(name):
    return name[:31]  # Truncate the name to 31 characters

# Set directory path
directory = "/Users/maxfroehner/Desktop/BMW_preprocessed"

# Get all .txt files in the directory
file_paths = glob.glob(os.path.join(directory, "*.txt"))

# Prepare a list to store DataFrames for Excel output
dfs = []

for file_path in file_paths:
    # Read file content
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Create dictionary and corpus for LDA
    dictionary = corpora.Dictionary([tokens])
    corpus = [dictionary.doc2bow(tokens)]
    
    # Perform LDA
    lda_model = LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
    
    # Extract topics
    topics = lda_model.print_topics(num_words=4)
    
    # Prepare data for DataFrame
    topic_data = {'Topic': [], 'Words': []}
    for topic_num, topic_words in topics:
        topic_data['Topic'].append(f'Topic {topic_num}')
        topic_data['Words'].append(topic_words)
    
    # Create DataFrame
    df = pd.DataFrame(topic_data)
    
    # Get the sheet name safely
    sheet_name = safe_sheet_name(os.path.basename(file_path))
    dfs.append((sheet_name, df))

# Write to Excel
with pd.ExcelWriter('/Users/maxfroehner/Desktop/LDA_Topics_BMW.xlsx') as writer:
    for sheet_name, df in dfs:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
