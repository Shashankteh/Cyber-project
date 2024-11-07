# Use an official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requriements.txt ./
RUN pip install --no-cache-dir -r requriements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose the port on which the app will run (matching Gradio’s configuration in app.py)
EXPOSE 3000

# Run the application
CMD ["python", "app.py"]
