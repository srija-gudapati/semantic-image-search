from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from backend import SemanticImageSearch

# Initialize FastAPI app
app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_methods=["*"],                     # Allow all HTTP methods
    allow_headers=["*"],                     # Allow all headers
)

# Mount the random-images directory to /images
app.mount("/images", StaticFiles(directory="random-images"), name="images")

# Initialize SemanticImageSearch with pre-indexed images
image_directory = "./random-images"
try:
    searcher = SemanticImageSearch(image_directory)
except ValueError as e:
    raise RuntimeError(f"Error initializing SemanticImageSearch: {e}")

# Pydantic model for query request
class SearchRequest(BaseModel):
    query: str
    top_k: int = Query(5, ge=1, le=25)  # Limit results between 1 and 25

# Pydantic model for query response
class SearchResult(BaseModel):
    image_path: str
    similarity_score: float

# API endpoint for querying similar images
@app.post("/search", response_model=List[SearchResult])
async def search_images(request: SearchRequest):
    try:
        results = searcher.search(query=request.query, top_k=request.top_k)
        # Prepend the full URL for the static images
        base_url = "http://127.0.0.1:8000/images/"
        return [
            {
                "image_path": f"{base_url}{path.split('/')[-1]}",
                "similarity_score": round(score, 3)
            }
            for path, score in results
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


