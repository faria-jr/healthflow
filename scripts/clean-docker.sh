#!/bin/bash
# Clean Docker to free up space

echo "🧹 Cleaning Docker..."

# Remove unused containers
docker container prune -f

# Remove unused images
docker image prune -f

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f

# Remove build cache
docker builder prune -f

echo "✅ Docker cleaned!"
echo ""
echo "💡 If you still have space issues:"
echo "   1. Increase Docker Desktop disk size (Settings > Resources > Disk)"
echo "   2. Run: docker system prune -a (WARNING: removes all unused data)"
