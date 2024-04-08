# Dockerfile for seasand-nectec-backend/point_cloud_project/

# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY ./point_cloud_project/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

# Copy the point_cloud_project code into the container
COPY ./point_cloud_project /app/point_cloud_project

# Command to run the application
CMD ["python", "/app/point_cloud_project/file.py"]
