import os
import numpy as np
from scipy.stats import entropy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
stop_words = stopwords.words('english')

# Function to load a single document from a file
def load_document_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to calculate entropy from a topic distribution
def calculate_entropy_from_topic_distribution(topic_distribution):
    probabilities = topic_distribution
    return entropy(probabilities, base=2)

# Function to perform LDA and calculate entropy
def lda_topic_modeling_with_entropy(document, n_topics=5, n_words=10):
    # Convert the document to a matrix of token counts
    vectorizer = CountVectorizer(stop_words=stop_words)
    dtm = vectorizer.fit_transform([document])
    
    # Perform LDA
    lda_model = LatentDirichletAllocation(n_components=n_topics, random_state=0)
    lda_model.fit(dtm)
    
    # Get topic-word distributions
    topic_word_distributions = lda_model.components_ / lda_model.components_.sum(axis=1)[:, np.newaxis]
    
    # Calculate entropy for each topic
    entropies = []
    for topic_dist in topic_word_distributions:
        entropies.append(calculate_entropy_from_topic_distribution(topic_dist))
    
    # Create a DataFrame to store the topics and entropies
    topics_df = pd.DataFrame({
        'Topic': [f'Topic {i}' for i in range(n_topics)],
        'Entropy': entropies
    })
    
    # Optionally, you can print out the top words in each topic
    feature_names = vectorizer.get_feature_names_out()
    topics_df['Top Words'] = [
        ' + '.join([f"{topic_dist[i]:.4f}*{feature_names[i]}" for i in topic_dist.argsort()[-n_words:][::-1]])
        for topic_dist in topic_word_distributions
    ]
    
    return topics_df

# Function to save the DataFrame to an Excel file with separate sheets and an average entropy summary
def save_topics_to_excel_with_avg_entropy(topics_dfs, avg_entropies, output_file):
    with pd.ExcelWriter(output_file) as writer:
        # Save each document's topics and entropies to separate sheets
        for file_name, topics_df in topics_dfs.items():
            sheet_name = os.path.splitext(file_name)[0][:31]  # Sheet names must be 31 characters or less
            topics_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Save the average entropies to a separate sheet
        avg_entropy_df = pd.DataFrame(list(avg_entropies.items()), columns=['File Name', 'Average Entropy'])
        avg_entropy_df.to_excel(writer, sheet_name='Average Entropy', index=False)

# Example usage
directory_path = '/Users/maxfroehner/Desktop/MB_preprocessed'  # Replace with the path to your .txt files
output_file = '/Users/maxfroehner/Desktop/MB_entropy.xlsx'  # Define the output file name

topics_dfs = {}
avg_entropies = {}

for filename in os.listdir(directory_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory_path, filename)
        document = load_document_from_file(file_path)
        topics_df = lda_topic_modeling_with_entropy(document, n_topics=5)
        
        # Calculate the average entropy for the document
        avg_entropy = topics_df['Entropy'].mean()
        avg_entropies[filename] = avg_entropy
        
        # Store the topics DataFrame
        topics_dfs[filename] = topics_df

# Save the DataFrame with results for each document and the average entropies to an Excel file
save_topics_to_excel_with_avg_entropy(topics_dfs, avg_entropies, output_file)

print(f"Output saved to {output_file}")
