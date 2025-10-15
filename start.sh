#!/bin/bash
# start.sh
echo "🚀 Setting up Iya Bola Assistant environment..."

# Install system packages
apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
pip install -r requirements.txt

echo "✅ Setup complete! Starting Streamlit app..."

# Start the Streamlit app on the Render-assigned port
streamlit run banking_iya_bola_App_Full.py --server.port=$PORT --server.address=0.0.0.0
