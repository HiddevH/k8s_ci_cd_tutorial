# docker_api_test

This repository contains a 'hello world' api to test Azure Data Factory webhook functionality with containerized API's deployed in K8s.

## Installation / Deployment

Use the requirements.txt or the environment.yml to create the environment with all neccesary packages.

```bash
conda create -f environment.yml
```

## Usage

```webhook
<ip>:5002/helloworld
```
Should return a json file with {'message': 'Hello World'}
