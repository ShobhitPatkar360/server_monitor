# Use the official Python image from Docker Hub
FROM python:3.13.3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install dependencies if requirements.txt exists
RUN pip install --no-cache-dir -r requirements.txt || true

# Command to run your Python script
CMD ["python", "app.py"]
