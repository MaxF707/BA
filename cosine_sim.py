import os
import chardet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openpyxl import Workbook  # Import openpyxl

# Function to read text from a file with automatic encoding detection
def read_file(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return raw_data.decode(encoding)

# Function to compute cosine similarity between two texts
def compute_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim[0][0]

# Directories containing the files
dir1 = '/Users/maxfroehner/Desktop/BMW_AI_answers'
dir2 = '/Users/maxfroehner/Desktop/BMW_questions_actual'

# Output file to save the results in Excel format
output_file = 'BMW_cosine_similarity_results.xlsx'

# List all files in both directories
files1 = sorted(os.listdir(dir1))
files2 = sorted(os.listdir(dir2))

# Ensure both directories have the same number of files
if len(files1) != len(files2):
    raise ValueError('Both directories must contain the same number of files.')

# Create a new workbook and select the active worksheet
wb = Workbook()
ws = wb.active
ws.title = "Cosine Similarity"

# Write header
ws.append(["File 1", "File 2", "Cosine Similarity"])

# Compute cosine similarity for each pair and write results to the worksheet
for file1, file2 in zip(files1, files2):
    file1_path = os.path.join(dir1, file1)
    file2_path = os.path.join(dir2, file2)
    text1 = read_file(file1_path)
    text2 = read_file(file2_path)
    similarity = compute_cosine_similarity(text1, text2)
    ws.append([file1, file2, similarity])

# Save the workbook
wb.save(output_file)

print(f'Cosine similarity results saved to {output_file}')
