# Corrected Dockerfile
FROM alpine:latest

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Expose port (adjust as needed)
EXPOSE 5002

# Run application
CMD ["python3", "app.py"]
