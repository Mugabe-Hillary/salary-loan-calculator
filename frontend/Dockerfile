# Use a slim Python base image for smaller image size
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies. Use --no-cache-dir to avoid caching wheel files
# and reduce image size, and --upgrade pip to ensure pip is up-to-date.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port Streamlit runs on (default is 8501)
EXPOSE 8501

# Command to run the Streamlit application
# The --server.port 8501 is important for Docker to expose the correct port
# The --server.headless true prevents opening a browser automatically in the container
# The --server.enableCORS false is set to false because we allow all origins from FastAPI.
# This prevents potential CORS issues from Streamlit itself when the frontend is running on non-localhost.
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]

