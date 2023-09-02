#  FastAPI Dockerized Application <snips.py>

This repository contains a FastAPI application that is Dockerized for easy deployment. Follow these steps to build and run the application.

## Prerequisites
Before you begin, ensure you have the following installed on your system:

Docker: Install Docker

### Build the Docker Image
Run the following command to build the Docker image for the FastAPI application:

```docker build -t snips-py:prod .```

### Run the Docker Container
Once the Docker image is built, you can create and run a Docker container with the following command:

```docker run -d -p 8000:8000 snips-py:prod```

### Access the FastAPI Application
You can access the FastAPI application in your web browser using the following URL:

```http://localhost:8000```

### Send a File via curl
To send a file to the FastAPI application using curl, you can use the following command:

`curl -X POST -F "file=@<path_to_file>" http://localhost:8000/upload/`

Replace `<path_to_file>` with the actual path to the file you want to upload.