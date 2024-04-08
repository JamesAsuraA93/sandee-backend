# # Use an official Python runtime as the base image for Python 3.9
# FROM python:3.9-slim AS python3.9

# # Set up environment variables
# ENV PYTHONUNBUFFERED 1

# # Create and set working directory
# WORKDIR /app

# # Install dependencies for the Python 3.9 environment
# COPY requirements.txt /app/requirements.txt
# RUN python -m venv venv3.9
# RUN /bin/bash -c "source venv3.9/bin/activate && pip install -r requirements.txt"

# # Copy your specific Python 3.9 code into the container
# COPY file.py /app/file.py

# # Use an official Python runtime as the base image for Python 3.10
# FROM python:3.10-slim AS python3.10

# # Set up environment variables
# ENV PYTHONUNBUFFERED 1

# # Create and set working directory
# WORKDIR /app

# # Install dependencies for the Python 3.10 environment
# COPY requirements.txt /app/requirements.txt
# RUN python -m venv venv3.10
# RUN /bin/bash -c "source venv3.10/bin/activate && pip install -r requirements.txt"

# # Copy the rest of the application code
# COPY . /app

# # Use an official Python runtime as the base image for the latest Python version
# FROM python:latest AS pythonLatest

# # Set up environment variables
# ENV PYTHONUNBUFFERED 1

# # Create and set working directory
# WORKDIR /app

# # Install dependencies for the latest Python version environment
# COPY requirements.txt /app/requirements.txt
# RUN python -m venv venvLatest
# RUN /bin/bash -c "source venvLatest/bin/activate && pip install -r requirements.txt"

# # Copy the rest of the application code
# COPY . /app

# # Set the command to run your Python application using FastAPI
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Dockerfile for seasand-nectec-backend/

# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY ./backend_api_project/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

# Copy the backend_api_project code into the container
COPY ./backend_api_project /app/backend_api_project

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend_api_project.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
