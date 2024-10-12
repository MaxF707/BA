import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Path to the directory containing documents
directory_path = '/Users/maxfroehner/Desktop/MB_transcripts_LDA'

# Create a new directory for the cleaned documents
cleaned_directory_path = os.path.join(directory_path, 'cleaned_documents')
os.makedirs(cleaned_directory_path, exist_ok=True)

# Function to process text
def process_text(text):
    # Remove non-informative text
    text = re.sub(r'\bladies and gentlemen\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(Björn Scheib|Bodo Uebber|Mercedes-Benz)\b', '', text, flags=re.IGNORECASE)
    
    # Tokenization
    tokens = word_tokenize(text.lower())
    
    # Remove punctuation and stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Rejoin tokens into a cleaned text
    cleaned_text = ' '.join(tokens)
    
    return cleaned_text

# Process each document in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        # Read the document
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as file:
            text = file.read()
        
        # Process the text
        cleaned_text = process_text(text)
        
        # Save the cleaned text to a new file in the cleaned_documents folder
        cleaned_file_path = os.path.join(cleaned_directory_path, filename)
        with open(cleaned_file_path, 'w') as file:
            file.write(cleaned_text)

print(f"Text processing complete. Cleaned files saved in the folder: {cleaned_directory_path}")
