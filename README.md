# CI/CD with Azure Pipelines and Kubernetes
This repository contains a 'hello world' api to test Azure Data Factory webhook functionality with containerized API's deployed in K8s. It is integrated into Azure Pipelines to explore that functionality as well.

Ideally we deploy this API as a serverless application, but thats still under construction :-).

### Repository contents
The repository is split into two folders, `app` and `deployment_config`. This is my vision on how the workflow should be with Azure Pipelines.

In the folder `app` you will find:
- The python script `api.py` which handles the actual API requests
- requirements.txt which contains the Python packages used
- Dockerfile with the instructions to build the container
- The pipeline YAML written to be used by Azure Pipelines

In the folder `deployment_config` you will find:
- The kubernetes deployment YAML
- The pipeline YAML written to be used by Azure Pipelines

## Application
Within the folder `app` there is a script called `api.py`. This script is basically a Flask application which listens on port `5002` for API requests.
The API requests possible are:
- `/helloworld` which returns a JSON `{"message":"Hello World"}`
- `/test` which returns a JSON `{"test":"test"}`

But it could also pass back a dataframe if thats your thing, this is just a minimal API version.

## Dockerfile
The API is supposed to live in a Docker container. A brief overview of its contents:
- Use the lightweight `python:3.7-slim-buster` distribution
- Copy requirements.txt and pip install on it
- Create a non-root User to run the scripts (according to some best practices found at https://pythonspeed.com/docker/)
- Copy the `api.py`
- Run the python script with argument `-p 5002` to run on port `5002`.

## Kubernetes  
The Kubernetes (k8s) deployment config is quite simple:
-  Run the container as mentioned earlier
-  Open up port `5002`
-  Create a service to allow internal traffic over port 5002 (if you choose a Load Balancer that will allow external traffic).

Note: There is a parameter `##BUILD_ID##` that will be filled in by Azure Pipelines as explained later on.

## Azure Pipeline
*Note: This is my view on running an efficient CI/CD Azure Pipeline, there might be other nicer solutions.*

 When I started with Azure Pipelines, I was using only two pipelines: one for build (CI) and one for release (CD). The build pipeline would trigger on a `git push` to master and start building a Docker container. Once finished the release pipeline would deploy the container to our K8s cluster. Unforeseen consequence was when I needed to play around with the K8s Deployment config, I would push my changes to master, the pipeline would start buidling a *new* version of the container. That was some quite extensive work for such a minor change. So building upon that knowledge I present you the following way of working.

 In this instance, there are three pipelines. The CI stage is seperated in two pipelines: one for dealing with changes in the application, and the other for dealing with changes in the K8s Deployment configuration. The CD stage only has one pipeline, which is supposed to push the container to AKS with the before mentioned K8s deployment config.
 The two CI pipelines have seperate triggers on directories within the master branch of de `k8s_ci_cd_tutorial` repo. Upon detecting a change in the `app` folder for instance, Azure Pipelines will start building a new Docker Image and push it to Azure Container Registry (ACR). All pipelines are written in YAML and stored in the repositories itself.

![alt text](https://i.postimg.cc/SKQrmzDP/CI-CD.jpg)

*Schematic overview of the CI/CD pipelines*

### Build (CI) Pipelines
Pushing a new version to the master branch will trigger an Azure Pipeline Build to execute depending on what folders have changes in them. The `app` pipeline triggers on a change in the **app** folder and builds a Docker Image using the Dockerfile in the directory, and pushes it to the ACR. The `deployment_config` pipeline triggers on a change in the **deployment_config** folder and builds a YAML Artifact.

### Release (CD) Pipeline
The Release Pipeline is triggered on two Artifacts. The first trigger is upon the appearance of a new Docker Image version in the Azure Container Registry. The second trigger is based upon a new version of the YAML Artifact (the k8s configuration). They are both scheduled to use the `Latest` version as default, and have the CD trigger on `Enabled`.

Then we have one stage in Release, with two tasks. The first task will retrieve the Build (version) number of the latest Docker Image (according to the CI) and inserts this as the `##BUILD_ID##` in the k8s deployment config.
```bash
# GET BUILD_ID from release artifact _API_TEST_HIDDE (the docker image) and SET the BUILD_ID parameter in the k8s-deployment.yml file

sed -i "s/##BUILD_ID##/${RELEASE_ARTIFACTS__K8S_CI_CD_TUTORIAL_BUILDNUMBER}/g" "$SYSTEM_ARTIFACTSDIRECTORY/_deploy_config_k8s_ci_cd_tutorial/deployment_config/k8s-deployment.yml"
```
 *Note: I actually wonder why not just use the `latest` version in de deployment config, but I can imagine this is more resilient.*

The final task will execute `kubectl apply` with *Use Configuration files* checked, pointing to the configuration file as given by the YAML Artifact.

## Result
By doing the above, you can update your application and k8s independently of each other. If you do something else (like writing this README), nothing on the CI/CD plane will happen (= good).

If the Pipelines executed succesfully, you can use kubectl to port forward the service to your workstation:

```bash
kubectl port-forward deployment/k8s_ci_cd_tutorial 5002:5002
```

This opens up a proxy with on port 5002 your API listening :-). Optionally, change the service to be a `Loadbalancer` to open up a public ip/port.


## Usage

```webhook
<ip>:5002/helloworld
```
Should return a json file with {'message': 'Hello World'}