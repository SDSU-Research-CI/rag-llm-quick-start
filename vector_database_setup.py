import csv, IPython.display, ollama, pip, os
from tqdm.notebook import tqdm
import chromadb, nltk
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
nltk.download("punkt", quiet = True) # Note: would be nice to load onto the notebook by default in the future to avoid this step
from nltk.tokenize import sent_tokenize

# This will clear the Chroma database
myfile = "/chroma/chroma.sqlite3"
# If file exists, delete it.
if os.path.isfile(myfile):
    os.remove(myfile)

# Collect student responses from CSV
# Test dataset included one qualitative question. TO DO: add the other questions
documents = []
with open("student_responses.csv", "r") as file:
  reader = csv.reader(file)
  for line in reader:
    text_response = line[0] # TO DO: add other fields and experiment with filters
    documents.append(text_response)

# Create vector database
client = chromadb.PersistentClient(path="/chroma",settings=Settings())
collection = client.create_collection(name = "docs")

# Vectorize responses by sentence-level chunks and store in vector database
for i, document in enumerate(documents):
  for j, sentence in enumerate(sent_tokenize(document)):
    response = ollama.embeddings(model = "nomic-embed-text", prompt = sentence)
    embedding = response["embedding"]
    collection.add(
      ids = [f"{i}_{j}"],
      embeddings = [embedding],
      documents = [document]
    )