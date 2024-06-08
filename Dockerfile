FROM tensorflow/tensorflow:2.16.1
WORKDIR /app
COPY requirements.txt .
# Install necessary dependencies
RUN pip install -r requirements.txt

# Copy model files into the container
COPY . .

# Set entrypoint
ENTRYPOINT ["python", "main.py"]