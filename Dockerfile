# Use a base Python image
FROM python:3.12-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your application will run on
EXPOSE 5000

# Command to run the application
CMD ["python", "youtube_downloader.py"]
