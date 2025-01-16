# Use a base Python image
FROM python:3.12-slim

# Install Chromium and dependencies, including a keyring for cookies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    fonts-liberation \
    gnome-keyring \
    libsecret-1-0 \
    && apt-get clean

# Create Chromium config directory
RUN mkdir -p /root/.config/google-chrome

# Set permissions for keyring
RUN chmod 700 /root/.config/google-chrome

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
