import gensim
from gensim import corpora
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Sample text (replace this with your earnings call text)
text = "Your earnings call transcript text here."

# Preprocess the text
stop_words = set(stopwords.words('english'))
tokens = [word for word in word_tokenize(text.lower()) if word.isalpha() and word not in stop_words]

# Create a dictionary and corpus
dictionary = corpora.Dictionary([tokens])
corpus = [dictionary.doc2bow(tokens)]

# Perform LDA
lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)

# Print the topics
topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(topic)
