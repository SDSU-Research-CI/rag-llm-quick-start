# rag-llm-quick-start

This quick start uses the Ollama software to host a model as well as Gradio to present a user interface you query information that's been embedded.

k create -f rag-llm-pod.yaml -n sdsu-mikefarley

k get pods -n sdsu-mikefarley

k exec -it -n sdsu-mikefarley rag-llm-ollama -- /bin/bash

k port-forward rag-llm-ollama -n sdsu-mikefarley 8888:7860

k cp -n sdsu-mikefarley student_responses.csv rag-llm-ollama:/root/code/data/student_responses.csv



1. pip install -r requirments.txt
2. curl -fsSL https://ollama.com/install.sh | sh

ollama serve &
ollama pull llama3
ollama pull nomic-embed-text

cd /root/code
mkdir data
mkdir chroma


