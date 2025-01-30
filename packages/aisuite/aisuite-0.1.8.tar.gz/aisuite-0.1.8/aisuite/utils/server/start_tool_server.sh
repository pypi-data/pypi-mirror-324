#!/bin/bash

# Set image name
IMAGE_NAME="tool-server"

# Check if the image already exists
if ! docker image inspect $IMAGE_NAME > /dev/null 2>&1; then
  # Build the image if it doesn't exist
  echo "Building Docker image..."
  docker build -t $IMAGE_NAME .
else
  echo "Docker image already exists, skipping build."
fi

# Run the container
echo "Running Docker container..."
docker run -p 7000:7000 $IMAGE_NAME

