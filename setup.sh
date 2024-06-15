#!/bin/bash

if [ ! -d "/chroma" ]; then
  echo "$DIRECTORY does not exist."
  mkdir /chroma
fi

pip install -r requirements.txt

curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3
ollama pull nomic-embed-text
