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

# Load the Excel file
file_path = '/Users/maxfroehner/Desktop/Questions_sperated.xlsx'  # Update this to the correct path
xl = pd.ExcelFile(file_path)

# Initialize a dictionary to store results
results_full = {}

# Process each company (BMW, VW, etc.)
for company in set(sheet.split('_')[0] for sheet in xl.sheet_names):
    # Load the sheets
    human_df = xl.parse(f'{company}_human')
    ai_df = xl.parse(f'{company}_AI')

    # Check if the company data is properly loaded
    if human_df.empty or ai_df.empty:
        print(f"Data missing for {company}, skipping...")
        continue

    # Assuming the questions are in a column named 'Questions' and the calls in a column named 'Call Name'
    human_questions = human_df['Questions']
    ai_questions = ai_df['Questions']
    calls = human_df['Call Name'].unique()

    company_results_full = []

    # For each call, calculate similarity scores
    for call in calls:
        human_call_questions = human_df[human_df['Call Name'] == call]['Questions'].tolist()
        ai_call_questions = ai_df[ai_df['Call Name'] == call]['Questions'].tolist()

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
                'Call': call,
                'AI_Question': ai_question,
                'Human_Question': best_match[0],
                'Similarity_Score': best_match[1]
            })

    # Save the results for the company
    if company_results_full:
        results_full[company] = company_results_full
    else:
        print(f"No results for {company}, skipping...")

# Write results to a new Excel sheet for all companies
output_file_path = '/Users/maxfroehner/Desktop/Word2Vec_results.xlsx'  # Update with your desired output path
with pd.ExcelWriter(output_file_path, mode='w', engine='openpyxl') as writer:
    for company, company_results_full in results_full.items():
        df_full = pd.DataFrame(company_results_full)
        
        # Ensure 'Call' column exists and is correct
        if 'Call' not in df_full.columns:
            print(f"'Call' column missing in {company} data, skipping average calculation...")
            df_full.to_excel(writer, sheet_name=f'{company}_Results', index=False)
            continue
        
        df_full.to_excel(writer, sheet_name=f'{company}_Results', index=False)

        # Calculate and write the average score per call
        avg_scores_full = df_full.groupby('Call')['Similarity_Score'].mean().reset_index()
        avg_scores_full.to_excel(writer, sheet_name=f'{company}_Averages', index=False)

print(f"Results have been saved to {output_file_path}")
