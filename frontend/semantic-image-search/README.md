# Frontend

This is the frontend for the PyTorch Semantic Image Search application. It is built using Next.js and styled with Tailwind CSS. Users can perform semantic image searches based on preloaded random images.

## Features

- User-friendly interface for text-based semantic search.
- Responsive design using Tailwind CSS.
- Connects to the FastAPI backend for fetching search results.

## Technologies Used

- **Framework**: Next.js
- **Styling**: Tailwind CSS
- **Language**: TypeScript

## Prerequisites

Before running the frontend, ensure you have the following installed:

- **Node.js**: [Download](https://nodejs.org/)

## Installation

1. Navigate to the `frontend/semantic-image-search` directory:

   ```bash
   cd frontend/semantic-image-search
   ```

2. Install the required dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`.

## Configuration

Make sure the backend is running at `http://127.0.0.1:8000` or update the API endpoint in the code if the backend runs on a different URL.

## Usage

1.  Open `http://localhost:3000` in your browser.
2.  Enter a text query (e.g., "sunset" or "mountains") and click "Search."
3.  View the matching images retrieved from the backend.
