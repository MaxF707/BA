from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Load the Excel file
file_path = '/path/to/your/Questions_sperated.xlsx'  # Update this to the correct path
xl = pd.ExcelFile(file_path)

# Initialize a dictionary to store results
results_full = {}

# Process each company (BMW, VW, etc.)
for company in set(sheet.split('_')[0] for sheet in xl.sheet_names):
    # Load the sheets
    human_df = xl.parse(f'{company}_human')
    ai_df = xl.parse(f'{company}_AI')

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

        # Vectorize the questions
        vectorizer = TfidfVectorizer().fit(human_call_questions + ai_call_questions)
        human_vectors = vectorizer.transform(human_call_questions)
        ai_vectors = vectorizer.transform(ai_call_questions)

        # Calculate cosine similarities
        similarity_matrix = cosine_similarity(ai_vectors, human_vectors)

        # For each AI question, find the most similar human question
        max_similarities = similarity_matrix.max(axis=1)
        for i, score in enumerate(max_similarities):
            company_results_full.append({
                'Call': call,
                'AI_Question': ai_call_questions[i],
                'Human_Question': human_call_questions[similarity_matrix[i].argmax()],
                'Similarity_Score': score
            })

    # Save the results for the company
    results_full[company] = company_results_full

# Write results to a new Excel sheet for all companies
output_file_path = '/path/to/output/Questions_Results_Cosine_Similarity.xlsx'  # Update with your desired output path
with pd.ExcelWriter(output_file_path, mode='w', engine='openpyxl') as writer:
    for company, company_results_full in results_full.items():
        df_full = pd.DataFrame(company_results_full)
        df_full.to_excel(writer, sheet_name=f'{company}_Results', index=False)

        # Calculate and write the average score per call
        avg_scores_full = df_full.groupby('Call')['Similarity_Score'].mean().reset_index()
        avg_scores_full.to_excel(writer, sheet_name=f'{company}_Averages', index=False)

print(f"Results have been saved to {output_file_path}")
