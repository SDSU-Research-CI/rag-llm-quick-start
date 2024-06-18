import chromadb, csv, nltk, ollama, os
from tqdm import tqdm
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
nltk.download("punkt", quiet = True)
from nltk.tokenize import sent_tokenize

# Remove old file, if applicable
if os.path.isfile("/chroma/chroma.sqlite3"):
    os.remove("/chroma/chroma.sqlite3")

# Collect student responses from CSV
questions, levels, years, colleges, time_bases, campuses, ages, residencies, living_situations, smart_devices, documents = [], [], [], [], [], [], [], [], [], [], []
with open("student_responses_all_detail.csv", "r") as file:
    reader = csv.reader(file)
    for line in reader:
        for i, var in enumerate((questions, levels, years, colleges, time_bases, campuses, ages, residencies, living_situations, smart_devices, documents)):
            var.append(line[i])

# Create vector database
client = chromadb.PersistentClient(path = "/chroma", settings = Settings())
collection = client.create_collection(name = "docs")

# Vectorize responses by sentence-level chunks and store in database
for i, document in enumerate(tqdm(documents)):
    for j, sentence in enumerate(sent_tokenize(document)):
        response = ollama.embeddings(model = "nomic-embed-text", prompt = sentence)
        embedding = response["embedding"]
        collection.add(
            ids = [f"{i}_{j}"],
            embeddings = [embedding],
            documents = [document],
            metadatas = [{"question": questions[i], "level": levels[i], "year": years[i], "college": colleges[i], 
                         "time_basis": time_bases[i], "campus": campuses[i], "age": ages[i], "residency": residencies[i],
                         "living_situation": living_situations[i], "smart_devices": smart_devices[i]}]
        )
