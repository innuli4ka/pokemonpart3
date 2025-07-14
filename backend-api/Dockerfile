# Use an official Python image
FROM python:3.12-slim

# Update system packages to fix vulnerabilities and remove unnecessary packages
RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get autoremove -y && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (for Docker cache efficiency)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY app.py .

# Expose Flask port
EXPOSE 5000

# Run your Flask app
CMD ["python", "app.py"]
