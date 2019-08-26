FROM python:3.7-slim-buster

COPY requirements.txt /tmp/

# Install app dependencies
RUN pip install -r /tmp/requirements.txt

# Create non-root User to run scripts
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Bundle app source
COPY api.py /src/

# K8s deployment configs
COPY deployment.yml /configs/

EXPOSE  5002
CMD ["python", "/src/api.py", "-p 5002"]
