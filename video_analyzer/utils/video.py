import os
import math
import hashlib
import requests

import numpy as np
from PIL import Image
import decord
# from decord import VideoReader, cpu
from logger import GLOBAL_LOGGER as log


def download_video(url, dest_path):
    response = requests.get(url, stream=True)
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8096):
            f.write(chunk)
    log.info(f"Video downloaded to {dest_path}")


def get_video_frames(video_path, num_frames=128, cache_dir='.cache'):
    # Expand ~ to user's home directory for cache_dir
    cache_dir = os.path.expanduser(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)
    
    # Handle video path
    if not (video_path.startswith(('http://', 'https://', '/', '~')) or '://' in video_path):
        # If it's a relative path, prepend ~/recordings
        recordings_dir = os.path.expanduser('~/recordings')
        video_path = os.path.join(recordings_dir, video_path)
    
    # Expand ~ in the final path if present
    video_path = os.path.expanduser(video_path)
    
    video_hash = hashlib.md5(video_path.encode('utf-8')).hexdigest()
    print(f"Processing video from: {video_path}")
    
    if video_path.startswith(('http://', 'https://')):
        video_file_path = os.path.join(cache_dir, f'{video_hash}.webm')
        if not os.path.exists(video_file_path):
            download_video(video_path, video_file_path)
    else:
        video_file_path = video_path
        
    return video_file_path