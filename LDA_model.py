import os
import gensim
from gensim import corpora
from gensim.models import LdaModel
import nltk
from nltk.corpus import stopwords
import string
import pandas as pd
import numpy as np

# Directory containing the documents
directory_path = '/Users/maxfroehner/Desktop/MB_transcripts_LDA'

# Ensure stopwords are downloaded
nltk.download('stopwords')

# Function to preprocess the text
def preprocess(text):
    tokens = gensim.utils.simple_preprocess(text)
    tokens = [token for token in tokens if token not in stopwords.words('english') and token not in string.punctuation]
    return tokens

# Function to calculate entropy (topic density)
def calculate_entropy(topic_distribution):
    # Only consider non-zero probabilities to avoid log(0) issues
    filtered_probs = [prob for _, prob in topic_distribution if prob > 0]
    return -sum(prob * np.log(prob) for prob in filtered_probs)

# List to hold results
results = []

# Loop through all files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory_path, filename)
        
        # Read and preprocess the document
        with open(file_path, 'r') as file:
            content = file.read()
            processed_text = preprocess(content)
        
        # Create a dictionary and corpus
        dictionary = corpora.Dictionary([processed_text])
        corpus = [dictionary.doc2bow(processed_text)]
        
        # Train the LDA model
        lda_model = LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
        
        # Get the topic distribution for the document
        document_topics = lda_model[corpus[0]]
        
        # Calculate the topic density (entropy)
        topic_density = calculate_entropy(document_topics)
        
        # Append the result
        results.append({
            'Filename': filename,
            'Topic Density': topic_density
        })

# Convert results to DataFrame and save to Excel
df = pd.DataFrame(results)
output_file = '/Users/maxfroehner/Desktop/MB_transcripts_LDA_topic_density.xlsx'
df.to_excel(output_file, index=False)

print(f"Results have been saved to {output_file}")
