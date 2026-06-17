# Use the official Python slim base image.
FROM python:3.11-slim

# Set the working directory inside the container.
WORKDIR /app

# Copy requirements first to take advantage of Docker layer caching.
COPY requirements.txt ./

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container.
COPY . /app

# Expose the port that Uvicorn will listen on.
EXPOSE 8000

# Start Uvicorn when the container launches.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
