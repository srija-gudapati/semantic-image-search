import requests
import os
import re

# Unsplash API key
# ACCESS_KEY = "Enter your Unsplash access key"

# Base URL for Unsplash API random photo endpoint
url = "https://api.unsplash.com/photos/random"

# Headers for authentication
headers = {"Authorization": f"Client-ID {ACCESS_KEY}"}

# Directory to save images
output_dir = "./random-images"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Function to sanitize filenames
def sanitize_filename(text: str) -> str:
    # Convert to lowercase, replace spaces with hyphens, and remove non-alphanumeric characters
    if text is None:
        return None
    text = text.lower().strip()
    text = re.sub(r"\s+", "-", text)  # Replace spaces with hyphens
    text = re.sub(r"[^a-z0-9\-]", "", text)  # Remove invalid characters
    return text

# Fetch and save 100 images in 4 batches
for i in range(2):
    print(f"Fetching batch {i + 1}...")
    
    # Set parameters to fetch 25 random images
    params = {"count": 25}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        images = response.json()  # List of image metadata
        
        for img in images:
            try:
                # Get the image URL (you can choose 'raw', 'full', or 'regular')
                img_url = img["urls"]["regular"]
                
                # Use the description as filename if available; fall back to the ID
                description = img.get("description", img.get("alt_description", "image"))
                filename = sanitize_filename(description) or img["id"]
                
                # Download the image
                img_data = requests.get(img_url).content
                
                # Save the image to the output directory
                file_path = os.path.join(output_dir, f"{filename}.jpg")
                with open(file_path, "wb") as f:
                    f.write(img_data)
                
                print(f"Saved: {file_path}")
            
            except Exception as e:
                print(f"Failed to save image: {e}")
    else:
        print(f"Error fetching images: {response.status_code}, {response.text}")

print(f"Images saved in: {output_dir}")
