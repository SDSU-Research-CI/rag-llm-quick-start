ARG BASE_IMAGE=nvidia/cuda:12.4.0-devel-ubuntu22.04

FROM ${BASE_IMAGE}

USER root
WORKDIR /root/src

# Install linux utils and dependencies
RUN apt-get update -y \
 && apt-get install -y --no-install-recommends \
    curl \
    vim \
    python3 \
    pip \
    pciutils \
    systemctl \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*

# Install and configure Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

RUN echo "[Unit]\nDescription=Ollama Service\n\nAfter=network-online.target\n\n[Service]\nExecStart=/usr/local/bin/ollama serve\nUser=ollama\nGroup=ollama\nRestart=always\nRestartSec=3\n\n[Install]\nWantedBy=default.target" \
    > /etc/systemd/system/ollama.service

RUN systemctl daemon-reload

USER ollama

ENV OLLAMA_KEEP_ALIVE=-1

USER root

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt \
 && rm requirements.txt

COPY ./*.py .
