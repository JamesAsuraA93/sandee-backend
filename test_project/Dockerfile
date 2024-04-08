# Dockerfile for seasand-nectec-backend/test_project/

# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY ./test_project/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

# Copy the test_project code into the container
COPY ./test_project /app/test_project

# Command to run the application
CMD ["python", "/app/test_project/main.py"]
