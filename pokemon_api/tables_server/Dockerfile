# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory
WORKDIR /app

# Set the PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Copy the requirements file from the root directory into the image
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire server directory contents into the image
COPY . .

# Expose the port FastAPI runs on
EXPOSE 5000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "tables_server:server", "--host", "0.0.0.0", "--port", "5000"]
