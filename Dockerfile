FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for opencv
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
# We can use standard opencv-python-headless
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY api/index.py .

# Configure rembg to use a writable directory for models
# Render allows writing to /tmp or we can use the home directory
ENV U2NET_HOME=/app/.u2net

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]
