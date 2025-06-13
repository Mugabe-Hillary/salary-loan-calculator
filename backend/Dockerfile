# Use a slim Python base image
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN apt update && \
    apt install -y curl && \ 
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Copy the entire backend application directory
# This copies app/main.py and app/models.py
COPY app/ app/

# Expose the port FastAPI runs on (default is 8000)
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
# --host 0.0.0.0 makes the app accessible from outside the container
# --port 8000 specifies the port within the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
