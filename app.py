import gradio as gr
import random
from langchain_community.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434"
CHROMA_PATH = "chroma/"
COLLECTION = "docs"
CHROMA_MODEL = "nomic-embed-text"

chroma_db = Chroma(collection_name=COLLECTION, persist_directory=CHROMA_PATH, embedding_function=OllamaEmbeddings(base_url=OLLAMA_URL, model=CHROMA_MODEL),)

def chat_ollama(message, history):
    # initiate ollama
    ollama = Ollama(base_url=OLLAMA_URL, model=OLLAMA_MODEL)

    # search for similar documents in chroma db
    result_chunks = chroma_db.similarity_search(message)
    
    chroma_knowledge = ""
    for id, chunk in enumerate(result_chunks):
        source_id = id + 1
        chroma_knowledge += "[" + str(source_id) +"] \n" + chunk.page_content + "\n"

    #sources = ""
    #for id, chunk in enumerate(result_chunks):
    #    source_id = id + 1
    #    sources += "[" + str(source_id) + "] \n" + chunk.metadata["source"] + "\n"

    #prompt = "Answer the following question using the provided knowledge and the chat history:\n\n###KNOWLEDGE: " + chroma_knowledge + "\n###CHAT-HISTORY: " + str(history) + "\n\n###QUESTION: " + message
    prompt = "Answer the following question using the provided knowledge and the chat history:\n\n###KNOWLEDGE: " + chroma_knowledge + "\n###CHAT-HISTORY: " + str(history) + "\n\n###QUESTION: " + message
    result = ollama(prompt) 

    # print(prompt)
    
    return result

#chat_ollama("What are you thoughts on AI in the classroom?", "")

gradio_interface = gr.ChatInterface(
        chat_ollama,
        chatbot=gr.Chatbot(),
        textbox=gr.Textbox(placeholder="Example: Who is Alice?", container=False, scale=7),
        title="The Ollama test chatbot",
        description=f"Ask the {OLLAMA_MODEL} chatbot a question!",
        theme='gradio/base', # themes at https://huggingface.co/spaces/gradio/theme-gallery
        retry_btn=None,
        undo_btn="Delete Previous",
        clear_btn="Clear",

)

gradio_interface.launch(auth=("user", "sdsu"))
