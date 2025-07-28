# Use the specified python base image compatible with AMD64 architecture
FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies that might be required by PyMuPDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the working directory
COPY . .

# Create input/output directories as specified in the run command context
RUN mkdir -p /app/input /app/output

# Set the command to run the main processing script
CMD ["python", "process_pdfs.py"]