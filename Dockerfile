FROM alpine:latest

# Update
RUN apk add --update python3.7 python3-pip

# Install app dependencies
RUN pip install -r requirements.txt

# Bundle app source
COPY api.py /src/api.py

EXPOSE  5002
CMD ["python", "/src/api.py", "-p 5002"]
