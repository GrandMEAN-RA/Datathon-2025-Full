#!/bin/bash
# setup.sh
echo "🚀 Setting up Iya Bola Assistant environment..."

# Install system packages if needed
apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
pip install -r requirements.txt

echo "✅ Setup complete!"
