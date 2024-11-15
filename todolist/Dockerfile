# Use the official Python image from the Docker Hub
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip3 install --no-cache-dir django

# Copy the Django project
COPY . .

RUN python3 manage.py makemigrations && python3 manage.py makemigrations api  && python3 manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]