FROM python:3.9
RUN pip install -r requirements.txt

# Update packages and install required dependencies
RUN apt-get update && \
    apt-get install -y g++ unixodbc-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Pyodbc
RUN pip install pyodbc

# Copy your application code to the container
COPY app.py /app/

# Set the working directory to the app directory
WORKDIR /app

# Run your application
CMD ["python", "app.py"]
