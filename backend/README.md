# Backend

This is the backend for the PyTorch Semantic Image Search application. It is built using FastAPI and powered by PyTorch. The backend provides the API for performing semantic image searches.

## Features

- Text-based semantic search using the CLIP model.
- API endpoints for searching preloaded images.
- Preloaded images stored in the `random-images` directory.

## Technologies Used

- **Framework**: FastAPI
- **Machine Learning**: PyTorch, Hugging Face Transformers
- **Language**: Python

## Prerequisites

Before running the backend, ensure you have the following installed:

- **Python 3.10+**: [Download](https://www.python.org/downloads/)

## Installation

1. Navigate to the `backend` directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:

   ```bash
   uvicorn call:app --reload
   ```

   The server will run at `http://127.0.0.1:8000`.

## Using Different Images

1.  Replace the images in the `random-images` directory by running the provided script:

    ```bash
    python get-random-images.py
    ```

    **Note**: You need an Unsplash Developer Access Key to use the script. Add it to the script by replacing the placeholder `ACCESS_KEY`.

2.  Alternatively, you can manually replace the images in the `random-images` folder.

## API Endpoints

- **`POST /search`**: Perform a semantic search on the preloaded images.

  - Request Body:

    ```json
    {
      "query": "your search text",
      "top_k": 5
    }
    ```

  - Response:
    ```json
    [
      {
        "image_path": "random-images/example.jpg",
        "similarity_score": 0.91 },
      ...
    ]
    ```
