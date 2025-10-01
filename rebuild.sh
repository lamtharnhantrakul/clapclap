#!/bin/bash
# Rebuild script for CLAP Docker container
# This script removes the cached model and rebuilds the Docker image

set -e

echo "======================================"
echo "CLAP Docker Rebuild Script"
echo "======================================"
echo ""

# Stop any running containers
echo "Stopping any running containers..."
docker-compose down 2>/dev/null || true

# Remove the model cache volume
echo "Removing model cache volume..."
docker volume rm clap-model-cache 2>/dev/null || true

# Rebuild the image
echo "Rebuilding Docker image..."
docker-compose build --no-cache

echo ""
echo "======================================"
echo "Rebuild complete!"
echo "======================================"
echo ""
echo "The model will be downloaded on the next run."
