# # # Dockerfile for seasand-nectec-backend/backend_api_project/

# # # Base image
# # # FROM python:3.9-slim
# # FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9



# # # Set environment variables
# # ENV PYTHONDONTWRITEBYTECODE 1
# # ENV PYTHONUNBUFFERED 1

# # # Set the working directory in the container
# # WORKDIR /app

# # # Copy the requirements file
# # COPY ./app/requirements.txt /app/requirements.txt

# # # Install dependencies
# # RUN pip install --upgrade pip && \
# #   pip install -r requirements.txt

# # # Copy the backend_api_project code into the container
# # COPY ./backend_api_project /app/backend_api_project

# # # Expose the port the app runs on
# # EXPOSE 8000

# # # Command to run the application
# # CMD ["uvicorn", "backend_api_project.app.main:app", "--host", "0.0.0.0", "--port", "8000"]




# # # FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# # # COPY ./app /app

# # Dockerfile
# # FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# # COPY ./app /app

# # Dockerfile
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# # Set working directory
# WORKDIR /app

# # Copy project files
# COPY ./app /app

# # Install additional dependencies
# RUN pip install --upgrade pip && \
#   pip install -r /app/requirements.txt

# RUN pip install motor

# # Expose port
# EXPOSE 80

# # Command to run the API server
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]



# Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY ./app /app

# Install additional dependencies
RUN pip install motor

# Expose port
EXPOSE 80

# Command to run the API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
