This is The Server for Video Analysis

## Setup
conda create -n qwen python=3.12 -y
conda activate qwen
pip install --upgrade uv
uv pip install vllm --torch-backend=auto
uv pip install -r requirements.txt


## Run the Server
./start_server.sh
