#!/bin/bash

cd /root

git clone https://github.com/SDSU-Research-CI/rag-llm-quick-start
mv rag-llm-quick-start code

cd code

pip install -r requirements.txt

curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3
ollama pull nomic-embed-text

if [ ! -d "/chroma" ]; then
  echo "$DIRECTORY does not exist."
  mkdir /chroma
fi
