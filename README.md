# FastAPI Application

Welcome to the kidlink backend! This project is a web API built with [FastAPI](https://fastapi.tiangolo.com/). It is used to make prediction of message classification and provide mail service.


## Requirements

- Python 3.7+
- pip (Python package installer)
- ubuntu os

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/kidlink-bangkit/kidlink-be.git
    cd kidlink-be
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the FastAPI server:**

    ```bash
    uvicorn main:app --reload
    ```

    By default, the server will run on `http://127.0.0.1:8000`.

## API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI:** Accessible at `http://127.0.0.1:8000/docs`
- **ReDoc:** Accessible at `http://127.0.0.1:8000/redoc`
