# Use an official Python runtime as a parent image
FROM python:3.12.9-alpine

# Set the working directory
WORKDIR /app

# Copy application files
COPY main.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure logs directory exists
RUN mkdir -p logs

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000
ENV FLASK_DEBUG=False
ENV FLASK_LOG_LEVEL=INFO
ENV FLASK_LOG_FILE=logs/app.log

# Run the application
CMD ["python", "main.py"]

