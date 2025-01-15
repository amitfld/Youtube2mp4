# Use a base Python image
FROM python:3.12-slim

# Install dependencies, including Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    fonts-liberation \
    && apt-get clean

# Set the Chromium path in environment variables
ENV CHROME_PATH="/usr/bin/chromium"

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
