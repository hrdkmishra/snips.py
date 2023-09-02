# Use the official Python Alpine image as the base image
FROM python:alpine3.18

# Expose port 8000 for FastAPI
EXPOSE 8000

# Create a working directory
WORKDIR /codespace

# Copy your FastAPI application code and web directory into the container
COPY . .

# Install the required Python packages and create a virtual environment
RUN python -m venv venv && \
    source venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt


# Start the FastAPI application using UVicorn within the virtual environment
CMD ["sh", "-c", "source venv/bin/activate && cd web/ && uvicorn main:app --host 0.0.0.0 --port 8000"]