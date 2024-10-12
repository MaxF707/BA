import gensim
import numpy as np
from scipy.spatial.distance import cosine
import pandas as pd

# Load the Google News Word2Vec model
model_path = '/Users/maxfroehner/Desktop/GoogleNews-vectors-negative300.bin'
word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)

# Function to compute the average word vector for a sentence
def sentence_vector(sentence, model):
    words = sentence.split()
    word_vectors = [model[word] for word in words if word in model]
    if not word_vectors:  # If no words in the model, return a zero vector
        return np.zeros(model.vector_size)
    return np.mean(word_vectors, axis=0)

# Load the BMW Excel file
file_path = '/Users/maxfroehner/Desktop/Questions_seperated_BMW.xlsx'  # Update this to the correct path
xl = pd.ExcelFile(file_path)

# Check the sheet names and column names to ensure consistency
print(xl.sheet_names)
bmw_human_df = xl.parse('BMW_human')
bmw_ai_df = xl.parse('BMW_AI')

print("BMW Human Columns:", bmw_human_df.columns)
print("BMW AI Columns:", bmw_ai_df.columns)

# Ensure the columns match expected names, and rename if necessary
bmw_human_df.columns = bmw_human_df.columns.str.strip()  # Strip any leading/trailing spaces
bmw_ai_df.columns = bmw_ai_df.columns.str.strip()

# Assuming the questions are in a column named 'Questions' and the calls in a column named 'CallName'
human_questions = bmw_human_df['Questions']
ai_questions = bmw_ai_df['Questions']
calls = bmw_human_df['CallName'].unique()

company_results_full = []

# For each call, calculate similarity scores
for call in calls:
    human_call_questions = bmw_human_df[bmw_human_df['CallName'] == call]['Questions'].tolist()
    ai_call_questions = bmw_ai_df[bmw_ai_df['CallName'] == call]['Questions'].tolist()

    # Skip if no questions are available in either list
    if not human_call_questions or not ai_call_questions:
        continue

    # Calculate similarity between AI and human questions
    for ai_question in ai_call_questions:
        ai_vector = sentence_vector(ai_question, word2vec_model)
        similarities = []
        for human_question in human_call_questions:
            human_vector = sentence_vector(human_question, word2vec_model)
            similarity_score = 1 - cosine(ai_vector, human_vector)
            similarities.append((human_question, similarity_score))

        # Find the human question with the highest similarity
        best_match = max(similarities, key=lambda x: x[1])
        company_results_full.append({
            'CallName': call,
            'AI_Question': ai_question,
            'Human_Question': best_match[0],
            'Similarity_Score': best_match[1]
        })

# Write results to a new Excel file for BMW
output_file_path = '/Users/maxfroehner/Desktop/BMW_Word2Vec_results.xlsx'  # Update with your desired output path
df_full = pd.DataFrame(company_results_full)

# Print columns to verify column names
print("df_full Columns:", df_full.columns)

with pd.ExcelWriter(output_file_path, mode='w', engine='openpyxl') as writer:
    df_full.to_excel(writer, sheet_name='BMW_Results', index=False)

    # Calculate and write the average score per call
    avg_scores_full = df_full.groupby('CallName')['Similarity_Score'].mean().reset_index()
    avg_scores_full.to_excel(writer, sheet_name='BMW_Averages', index=False)

print(f"BMW Results have been saved to {output_file_path}")
