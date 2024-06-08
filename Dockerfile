FROM tensorflow/tensorflow:2.16.1
WORKDIR /app
COPY requirements.txt .
# Install necessary dependencies
RUN pip install -r requirements.txt --no-cache-dir --upgrade

# Copy model files into the container
COPY . .

# Set entrypoint
CMD ["fastapi", "run", "main.py", "--port", "80"]
