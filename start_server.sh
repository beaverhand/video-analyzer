#!/bin/bash
# Activate conda environment and start server

# Load Conda into the shell
source /home/bornouksyn/miniconda3/etc/profile.d/conda.sh

# Activate the environment
conda activate qwen

# Load only VLLM_PORT from .env
# Load .env variables
set -a                   # automatically export all variables
source /home/bornouksyn/video-analyzer/.env
set +a                   # stop auto-exporting

echo "VLLM_PORT is $VLLM_PORT"

# Optionally wait for CUDA to be ready
echo "Waiting for CUDA..."
until nvidia-smi &>/dev/null; do
  echo "CUDA not ready yet, retrying in 2s..."
  sleep 2
done
echo "CUDA is ready"

# Prepare log directory
LOG_DIR="/home/bornouksyn/video-analyzer/logs"
mkdir -p "$LOG_DIR"

# Create separate log files
VLLM_LOG="$LOG_DIR/vllm_server_$(date +'%Y%m%d_%H%M%S').log"
ANALYZER_LOG="$LOG_DIR/video_analyzer_$(date +'%Y%m%d_%H%M%S').log"

# Start vLLM server (background)
echo "🚀 Starting vLLM server..."
vllm serve $MODEL \
  --port $VLLM_PORT \
  --tensor-parallel-size 1 \
  --max-num-batched-tokens 16384 \
  --max-num-seqs 8 \
  --disable-log-requests \
  > "$VLLM_LOG" 2>&1 &

VLLM_PID=$!

# Wait for vLLM to be ready
echo "⌛ Waiting for vLLM server to be ready..."
until curl -s http://127.0.0.1:8000/v1/models &>/dev/null; do
  echo "vLLM not ready yet, retrying in 3s..."
  sleep 3
done
echo "✅ vLLM server is ready with $MODEL"

# Start video analyzer (foreground or background)
echo "🚀 Starting video analyzer server..."
python /home/bornouksyn/video-analyzer/video_analyzer/server.py \
  > "$ANALYZER_LOG" 2>&1 &

ANALYZER_PID=$!

# Keep script alive until either process exits
wait -n

# Clean up when one stops
echo "🛑 Shutting down vLLM server..."
kill $VLLM_PID $ANALYZER_PID 2>/dev/null