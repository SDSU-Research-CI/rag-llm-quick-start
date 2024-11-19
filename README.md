# RAG LLM Quick Start

This examples illustrates the use of retrieval augmented generation (RAG) and large languages models (LLMs) to query and uncover answers about data not part of the LLMs corpus of knowledge.

The quick starts uses Ollama as the tool for downloading and hosting models. In this example, the llama 3 model is used. Gradio is used to present a web-based chat interface.

Steps to deploy the quick start:

## Clone repository

Clone this repository to your local machine where you have a working *kubectl* installation with a recent "config" file from the Nautilus Portal.

**Note:** You will need access to a Nautilus Namespace. Replace *\<namespace\>* below with your namespace.

## Create persistent PVC (disk) 
Create a persistent PVC (disk) to hold the vector database. This example uses Chroma, which is a sqllite, disk-based database. This is a one-time step, or if you need to update the vector store with new data.

```
kubectl create -f rag-llm-chroma.yaml -n <namespace>
```

The chroma PVC will be mounted to /chroma on the running container. This path/disk is persistent, unlike the container image's file system which is ephemeral. 

**Note:** You may wish to edit the yaml to increase the file storage size. 10GB is used as a starting point. Also note the example targets block storage on CSU TIDE hardware.

## Set a password

The Gradio web interface is protected with a username and pasword. The username is hardcoded as "user" and the password is read in from a secret. Use the following command to set a secret password in your namespace, replacing \<password\> with your desired password:

```
kubectl create -n <namespace> secret generic webpass --from-literal=password=<password>
```

## Create deployment

Create the deployment:

```
kubectl create -f rag-llm-deployment.yaml -n <namespace>
```

This step will start the container and run several commands identified in the yaml file, including starting Ollama, downloading models, and run the app.py program which will serve up the Gradio-based web interface.

However, we must first initialize the Chroma database with our data to be used for RAG.

Check that the deployment successfully created and a new rag-llm-ollama pod started:

```
kubectl get pods -n <namespace>
```

The above command should return a pod 

```
NAME                   READY   STATUS    RESTARTS   AGE
rag-llm-ollama-6c7d454b5-t5jwq   1/1     Running   0          35m
```

**Note:** The text after the *rag-llm-ollama-* pod name will be unique and you'll need it for the next steps.

## Connect to the pod's terminal

Using the pod name identified above, run the follow command to connect to the pod's terminal:

```
kubectl exec -it -n <namespace> rag-llm-ollama-<unique>-<name> -- /bin/bash
```

If the above works, you'll be presented with root shell prompt in the running container. 

E.g., 

```
root@rag-llm-ollama-123456789-12345:/# hostname
rag-llm-ollama-12345

root@rag-llm-ollama-123456789-12345:/# whoami
root
````

## Populate the Chroma database

Change to the src directory in root's home directory:

```
cd ~/src/
```

This directory contains all the python files from this repository when the container was built.
If you have changed these files, than another version of the container needs to be built to include these latest changes.

Next, open a second terminal on your local machine where your RAG data file is located. In this example, we have a CSV file named student_responses.csv that we want to use for RAG. 

The following command file copy the student_responses.csv file from your local computer to src directory on the remote container:

```
kubectl cp -n <namespace> student_responses.csv rag-llm-ollama-<unique>-<name>:/root/src/student_responses.csv
```

Return to the remote shell and issue a directory list command. You should now see the student_responses.csv file in the directory.

```
root@rag-llm-ollama-123456789-12345:~/src# ls -la
...
-rw-r--r-- 1 root root 1240 Jun 17 20:04 student_responses.csv
...
```

Next, use the vector_database_setup.py Python program to populate the Chroma database on the persistent /chroma storage.

```
python3 vector_database_setup.py
```

This command may take 5-10 minutes depending on document size. You can monitor the progress running the following command your second terminal window:

```
kubectl logs rag-llm-ollama-<unique>-<name> -n <namespace>
```

This will return the console output from the container and is handy for troubleshooting.

## Restart the deployment

Once the Chroma database has been created, you will want to essentially recreate the deployment.

```
kubectl delete deployment rag-llm-ollama -n <namespace>
kubectl create -f rag-llm-deployment.yaml -n <namespace>
```

The above command would also be run if you make updates to app.py or vector_database_setup.py and build a new version of the container and want the new code to be deployed.
After building and pushing the new container image, you would need to update line 34 with the new image URL.
Then you can apply the updated deployment with the commands above.

## Create service and ingress

The following steps only need to be executed once and will set up a service and ingress for the deployment. This is what will make the web interface accessible:

Create the service:

```
kubectl create -f rag-llm-service.yaml -n <namespace>
```

Create the ingress point:

```
kubectl create -f rag-llm-ingress.yaml -n <namespace>
```

Note: The endpoint URL is defined in two place in the service if you wish to change it.

## Other useful commands

You don't need to run these commands, just listing a few that might be handy in the future.

## Clean up / delete resources

### Deployment/pod
If you wish to stop the deployment/pod to free up resources, you can run the following command:

```
kubectl delete -f rag-llm-deployment.yaml -n <namespace>

```

Once complete, you can check that the deployment is delete by running:

```
kubectl get deployments -n <namespace>
kubectl get pods -n <namespace>

```

### Port forwarding ###

If you wish to connect to a port running in a container without setting up service/ingress, you can do a port forward between the specific pod and your computer. In the example below, you are forwarding port 8888 on your local host to port 7860 on the container, so you would be able to use your web browser running on your computer to connect to http://localhost:8888 to reach the remote app.

```
kubectl port-forward rag-llm-ollama-123456789-1234 -n <namespace> 8888:7860
```

