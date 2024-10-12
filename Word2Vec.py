#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:01:30 2024

@author: maxfroehner
"""

import gensim.downloader as api
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Function to preprocess text
def preprocess(text):
    # Remove non-alphabet characters and tokenize
    text = re.sub(r'[^A-Za-z\s]', '', text)
    tokens = text.lower().split()
    return tokens

# Load the word2vec model
model = api.load('word2vec-google-news-300')

# Function to convert text to vector
def text_to_vector(text, model):
    tokens = preprocess(text)
    # Get vectors for each token
    vectors = [model[word] for word in tokens if word in model]
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(300)

# Load the text from the files
with open('/mnt/data/2024-Mar-13-VOWG.DE-140192337307-Transcript.txt', 'r') as file1:
    text1 = file1.read()

with open('/mnt/data/2023-Oct-26-VOWG.DE-138579122026-Transcript.txt', 'r') as file2:
    text2 = file2.read()

# Convert texts to vectors
vector1 = text_to_vector(text1, model)
vector2 = text_to_vector(text2, model)

# Calculate cosine similarity
similarity = cosine_similarity([vector1], [vector2])

similarity[0][0]
