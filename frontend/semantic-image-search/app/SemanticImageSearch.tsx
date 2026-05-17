"use client";

import React, { useState, FormEvent, ChangeEvent, useEffect } from "react";
import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

// Types
interface ImageResult {
  image_path: string;
  similarity_score: number;
}

const fetchSimilarImages = async (
  query: string,
  count: number
): Promise<ImageResult[]> => {
  const response = await fetch("/api/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, top_k: count }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch images");
  }

  return await response.json();
};

// Main component
const SemanticImageSearch = () => {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [resultCount, setResultCount] = useState<number>(12);
  const [images, setImages] = useState<ImageResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Load initial images with empty query
  useEffect(() => {
    (async () => {
      try {
        const initialImages = await fetchSimilarImages("", 12);
        setImages(initialImages);
      } catch (error) {
        console.error("Error loading initial images:", error);
      }
    })();
  }, []);

  const handleSearch = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const results = await fetchSimilarImages(searchQuery, resultCount);
      setImages(results);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCountChange = (e: ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    if (!isNaN(value) && value >= 1 && value <= 100) {
      setResultCount(value);
    }
  };

  return (
    <div className="w-full mx-auto p-4 space-y-6 min-h-screen bg-gray-50">
      <div className="relative text-center py-4">
        <h1 className="text-3xl font-bold text-gray-800">
          <p className="inline-flex text-orange-600">PyTorch</p> Semantic Image
          Search
        </h1>
        <p className="text-gray-600 mt-2">
          Search through a random collection of images
        </p>
        <a
          href="https://github.com/your-repo-link"
          target="_blank"
          rel="noopener noreferrer"
          className="absolute top-4 right-4 text-gray-800 hover:text-black"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5c.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34c-.46-1.16-1.11-1.47-1.11-1.47c-.91-.62.07-.6.07-.6c1 .07 1.53 1.03 1.53 1.03c.87 1.52 2.34 1.07 2.91.83c.09-.65.35-1.09.63-1.34c-2.22-.25-4.55-1.11-4.55-4.92c0-1.11.38-2 1.03-2.71c-.1-.25-.45-1.29.1-2.64c0 0 .84-.27 2.75 1.02c.79-.22 1.65-.33 2.5-.33s1.71.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02c.55 1.35.2 2.39.1 2.64c.65.71 1.03 1.6 1.03 2.71c0 3.82-2.34 4.66-4.57 4.91c.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2"
            />
          </svg>
        </a>
      </div>

      <form
        onSubmit={handleSearch}
        className="flex flex-col sm:flex-row gap-4 bg-white p-4 rounded-lg shadow-sm"
      >
        <div className="relative flex-1">
          <Input
            type="text"
            placeholder="Try searching 'scene' or any other keyword..."
            value={searchQuery}
            onChange={(e: ChangeEvent<HTMLInputElement>) =>
              setSearchQuery(e.target.value)
            }
            className="pl-10 w-full"
          />
          <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>

        <div className="flex gap-4">
          <Input
            type="number"
            min={1}
            max={25}
            value={resultCount}
            onChange={handleCountChange}
            className="w-24"
            placeholder="Count"
          />
          <Button
            type="submit"
            disabled={isLoading}
            className={`min-w-[100px] ${isLoading ? "opacity-70" : ""}`}
          >
            {isLoading ? "Loading..." : "Search"}
          </Button>
        </div>
      </form>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {images.map((image: ImageResult, index) => (
          <Card
            key={index}
            className="overflow-hidden hover:shadow-lg transition-shadow duration-300"
          >
            <CardContent className="p-0">
              <img
                src={image.image_path}
                alt={`Result ${index + 1}`}
                className="w-full h-full object-cover aspect-square hover:scale-105 transition-transform duration-300"
                loading="lazy"
              />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default SemanticImageSearch;
