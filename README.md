# snips.py

![image](images\2023-09-04_16-50.png)

This repository is a FastAPI application that is Dockerized for easy deployment and hosting. The application allows you to upload file from your terminal to share your code just like a pastebin without using pastebin :p

>**This is a *Python implementation* of [snips.sh](https://github.com/robherley/snips.sh/) which is written in *Go***

>**Follow these steps to build and run the application.**

## Manual Installation

```
git clone https://github.com/hrdkmishra/snips.py.git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn web/main:app --reload
```


## Docker Installation

### Before you begin, ensure you have the following installed on your system:

`Docker: Install Docker`

### Build the Docker Image
Run the following command to build the Docker image for the FastAPI application:

`docker build -t snips-py:prod .`

### Run the Docker Container
Once the Docker image is built, you can create and run a Docker container with the following command:

`docker run -d -p 8000:8000 snips-py:prod`

### Access the FastAPI Application
You can access the FastAPI application in your web browser using the following URL:
```http://127.0.0.1:8000```

### Send a File via curl
To send a file to the FastAPI application using curl, you can use the following command:

`curl -X POST -F "file=@<path_to_file>" http://127.0.0.1:8000/upload/`

Replace `<path_to_file>` with the actual path to the file you want to upload.
