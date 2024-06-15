#!/bin/bash

if [ ! -d "/chroma" ]; then
  echo "$DIRECTORY does not exist."
  mkdir /chroma
fi

apt-get update
apt-get install -y vim

pip install -r requirements.txt

curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
sleep 60
ollama pull llama3
ollama pull nomic-embed-text
