from pathlib import Path
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from typing import List, Tuple

class SemanticImageSearch:
    def __init__(self, image_directory: str = None):
        """
        Initialize the semantic image search system using Hugging Face's transformers.
        
        Args:
            image_directory (str, optional): Directory containing images to index.
        """
        # Automatically set device based on availability
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Load CLIP model and processor
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        # Initialize empty image database
        self.image_paths: List[str] = []
        self.image_embeddings: torch.Tensor = None
        
        # If directory provided, index all images
        if image_directory:
            self.index_directory(image_directory)
    
    def process_image(self, image_path: str) -> torch.Tensor:
        """Load and preprocess a single image."""
        image = Image.open(image_path).convert('RGB')
        return image
    
    @torch.no_grad()
    def compute_image_embedding(self, images: List[Image.Image]) -> torch.Tensor:
        """Compute CLIP image embeddings."""
        inputs = self.processor(images=images, return_tensors="pt", padding=True).to(self.device)
        image_features = self.model.get_image_features(**inputs)
        # Normalize embeddings
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        return image_features
    
    @torch.no_grad()
    def compute_text_embedding(self, text: str) -> torch.Tensor:
        """Compute CLIP text embedding for a query."""
        inputs = self.processor(text=[text], return_tensors="pt", padding=True).to(self.device)
        text_features = self.model.get_text_features(**inputs)
        # Normalize embeddings
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        return text_features
    
    def index_directory(self, directory: str) -> None:
        """Index all images in a directory."""
        image_files = list(Path(directory).rglob("*.[jp][pn]g"))
        
        images = []
        valid_paths = []
        
        for image_path in image_files:
            try:
                image = self.process_image(image_path)
                images.append(image)
                valid_paths.append(str(image_path))
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
        
        if not images:
            raise ValueError("No valid images found in directory.")
        
        # Compute embeddings for all images
        self.image_embeddings = self.compute_image_embedding(images)
        self.image_paths = valid_paths
    
    @torch.no_grad()
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for images matching the text query.
        
        Args:
            query (str): Text query.
            top_k (int): Number of results to return.
            
        Returns:
            list: List of (image_path, similarity_score) tuples.
        """
        if self.image_embeddings is None:
            raise ValueError("No images indexed yet.")
        
        # Compute text embedding
        text_embedding = self.compute_text_embedding(query)
        
        # Compute similarities
        similarities = (self.image_embeddings @ text_embedding.T).squeeze()
        
        # Get top-k indices
        top_similarities, top_indices = similarities.topk(min(top_k, len(self.image_paths)))
        
        # Return results
        results = [
            (self.image_paths[idx], score.item())
            for idx, score in zip(top_indices, top_similarities)
        ]
        
        return results
