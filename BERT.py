import os
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Paths to directories
questions_dir = '/Users/maxfroehner/Desktop/BMW_questions_actual'
answers_dir = '/Users/maxfroehner/Desktop/BMW_AI_answers'

# Load pre-trained model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = BertModel.from_pretrained('bert-base-cased')

# Function to read text file
def read_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

# Function to get BERT embeddings
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()

# DataFrame to store results
results = []

# List files from both directories
question_files = sorted(os.listdir(questions_dir))
answer_files = sorted(os.listdir(answers_dir))

# Iterate through corresponding files in both directories
for question_file, answer_file in zip(question_files, answer_files):
    question_path = os.path.join(questions_dir, question_file)
    answer_path = os.path.join(answers_dir, answer_file)

    # Read the contents
    question_text = read_text(question_path)
    answer_text = read_text(answer_path)

    # Get embeddings
    question_embedding = get_embedding(question_text)
    answer_embedding = get_embedding(answer_text)

    # Calculate cosine similarity
    similarity = cosine_similarity(
        question_embedding.reshape(1, -1),
        answer_embedding.reshape(1, -1)
    )[0][0]

    # Append result
    results.append({
        'Question File': question_file,
        'Answer File': answer_file,
        'Similarity': similarity
    })

# Convert results to DataFrame
df = pd.DataFrame(results)

# Save to Excel file
output_path = '/Users/maxfroehner/Desktop/BMW_similarity_scores_BERT.xlsx'
df.to_excel(output_path, index=False)
