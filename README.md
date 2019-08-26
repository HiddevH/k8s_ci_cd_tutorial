# docker_api_test
This repository contains a 'hello world' api to test Azure Data Factory webhook functionality with containerized API's deployed in K8s.

-> Elaborate on the split between 'app' and 'deployment_configs'

## Azure Pipeline
Committing to the master branch of this repo will trigger the pipeline. Deploying to k8s will be like this:
https://cloudblogs.microsoft.com/opensource/2018/11/27/tutorial-azure-devops-setup-cicd-pipeline-kubernetes-docker-helm/

![alt text](https://cloudblogs.microsoft.com/uploads/prod/sites/37/2018/11/AzureDevOps-overview.png)

## Local Installation

Use the requirements.txt or the environment.yml to create the environment with all neccesary packages.

```bash
conda create -f environment.yml
```
then hop to the environment 
```bash
conda activate <environment>
```

you can run the server like this:
```bash
python api.py -p 5002
```

## Deploying in k8s
In the Dockerfile are the instructions for docker to build the app. It runs on a lightweight Linux distribution with Python and creates an environment using the requirements.txt (avoided the need of Conda in this case).
You need docker to build the image.. 


## Usage

```webhook
<ip>:5002/helloworld
```
Should return a json file with {'message': 'Hello World'}
