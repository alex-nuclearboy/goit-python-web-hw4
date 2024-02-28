# Use the Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the content of your project into the working directory of the container
COPY . /app

# Specify the port to be exposed by the container
EXPOSE 3000

# Define the volume to persist data
VOLUME ["/app/storage"]

# Command to run your application
CMD ["python", "main.py"]
