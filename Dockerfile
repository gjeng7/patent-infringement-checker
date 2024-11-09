# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expose port 5000 for Flask
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run"]
