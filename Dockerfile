# Dockerfile

# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Set environment variables (adjust according to your configuration)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Run the migration and then start the application
CMD ["sh", "-c", "flask db upgrade && flask run --host=0.0.0.0"]
