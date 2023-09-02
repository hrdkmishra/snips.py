# Use the official Python Alpine image as the base image
FROM python:alpine3.18

# Create a non-root user
RUN adduser -D -s /bin/false nonrootuser

# Expose port 8000 for FastAPI
EXPOSE 8000

# Define environment variables for external access (set to localhost)
ENV SNIPS_HTTP_EXTERNAL=http://localhost:8000

# Create a working directory
WORKDIR /codespace

# Copy your FastAPI application code and web directory into the container
COPY . .


# Start the FastAPI application using UVicorn within the virtual environment
CMD ["sh", "-c", "python -m venv venv && source venv/bin/activate && pip install --no-cache-dir -r requirements.txt && cd web/ && uvicorn main:app --host 0.0.0.0 --port 8000"]
