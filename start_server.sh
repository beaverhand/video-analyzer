#!/bin/bash
# Activate conda environment and start server

# Load Conda into the shell
source /home/bornouksyn/miniconda3/etc/profile.d/conda.sh

# Activate the environment
conda activate qwen

# Optionally wait for CUDA to be ready
echo "Waiting for CUDA..."
until nvidia-smi &>/dev/null; do
  echo "CUDA not ready yet, retrying in 2s..."
  sleep 2
done
echo "CUDA is ready"

# Start the server
echo "Starting server..."
exec python /home/bornouksyn/video-analyzer/video_analyzer/server.py
