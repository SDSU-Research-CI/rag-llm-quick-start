# rag-llm-quick-start

This quick start uses the Ollama software to host a model as well as Gradio to present a user interface you query information that's been embedded.

k create -f rag-llm-pod.yaml -n sdsu-mikefarley

k get pods -n sdsu-mikefarley

k exec -it -n sdsu-mikefarleyrag-llm-ollama -- /bin/bash

k port-forward rag-llm-ollama -n sdsu-mikefarley 8888:7860