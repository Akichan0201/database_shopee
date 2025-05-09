# Use an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY test.py .

# Set the command to run the script
CMD ["python", "test.py"]
