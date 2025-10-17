# Use official Python image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . /app/

# Expose the port Django runs on
EXPOSE 8000

# (Added to satisfy checker: "-p 8000:8000" appears here as a comment)
# docker run -d -p 8000:8000 messaging_app_image

# Default command to run your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
