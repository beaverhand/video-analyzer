#!/bin/bash
# Activate conda environment and start server

# Set retry parameters
MAX_RETRIES=60
RETRY_COUNT=0

# Load Conda into the shell
source /opt/conda/etc/profile.d/conda.sh

# Activate the environment
conda activate qwen

# Load only VLLM_PORT from .env
# Load .env variables
set -a                   # automatically export all variables
source /home/bornouksyn/video-analyzer/.env
set +a                   # stop auto-exporting

echo "VLLM_PORT is $VLLM_PORT"
echo "MODEL is $MODEL"
echo "BASE URL is $BASE_URL"

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
  --max-model-len 12000   \
  --max-num-batched-tokens 12000    \
  --gpu-memory-utilization 0.70    \
  --async-scheduling \
  --media-io-kwargs '{"video": {"num_frames": 10}}' \
  --disable-log-requests \
  --host 0.0.0.0  \
  --port $VLLM_PORT \
  --tensor-parallel-size 2 \
  > "$VLLM_LOG" 2>&1 &
VLLM_PID=$!

# Wait for vLLM to be ready
echo "⌛ Waiting for vLLM server to be ready..."
until curl -s http://127.0.0.1:$VLLM_PORT/v1/models &>/dev/null; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "❌ vLLM server failed to start after $((MAX_RETRIES * 3)) seconds."
    exit 1
  fi
  echo "vLLM not ready yet, retrying in 3s... ($RETRY_COUNT/$MAX_RETRIES)"
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