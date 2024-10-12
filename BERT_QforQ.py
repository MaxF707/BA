import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Load the tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = BertModel.from_pretrained('bert-base-cased')

# Function to compute BERT embeddings
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512, clean_up_tokenization_spaces=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

# Load the Excel file
file_path = '/Users/maxfroehner/Desktop/Questions_seperated_MB.xlsx'
xls = pd.ExcelFile(file_path)

# Initialize a DataFrame to store results
results = []

# Load the sheets with corrected column names
human_df = pd.read_excel(xls, sheet_name='MB_human')
ai_df = pd.read_excel(xls, sheet_name='MB_AI')

# Trim spaces in CallName fields
human_df['CallName'] = human_df['CallName'].str.strip()
ai_df['CallName'] = ai_df['CallName'].str.strip()

# Process the data separately for each call
for call in human_df['CallName'].unique():
    human_questions = human_df[human_df['CallName'] == call]['Questions'].tolist()
    ai_questions = ai_df[ai_df['CallName'] == call]['Questions'].tolist()

    if not human_questions or not ai_questions:
        print(f"No questions found for call: {call}")
        continue

    for ai_question in ai_questions:
        ai_embedding = get_bert_embedding(ai_question)

        # Calculate similarity scores
        max_score = 0
        best_match = None
        for human_question in human_questions:
            human_embedding = get_bert_embedding(human_question)
            score = cosine_similarity(ai_embedding, human_embedding)[0][0]
            if score > max_score:
                max_score = score
                best_match = human_question

        # Save the best match and score
        results.append({
            'CallName': call,
            'AI Question': ai_question,
            'Human Question': best_match,
            'Similarity Score': max_score
        })

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Ensure column names are strings and strip any whitespace
results_df.columns = results_df.columns.astype(str).str.strip()

# Calculate average score per call
if not results_df.empty:
    average_scores = results_df.groupby(['CallName'])['Similarity Score'].mean().reset_index()

    # Save the results and average scores to a new Excel file
    output_path = '/Users/maxfroehner/Desktop/MB_BERT_scores.xlsx'
    with pd.ExcelWriter(output_path) as writer:
        results_df.to_excel(writer, sheet_name='Pairing Scores', index=False)
        average_scores.to_excel(writer, sheet_name='Average Scores', index=False)
else:
    print("No data to save. The results DataFrame is empty.")
