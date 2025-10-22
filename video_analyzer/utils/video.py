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
    os.makedirs(cache_dir, exist_ok=True)

    video_hash = hashlib.md5(video_path.encode('utf-8')).hexdigest()
    if video_path.startswith('http://') or video_path.startswith('https://'):
        video_file_path = os.path.join(cache_dir, f'{video_hash}.mov')
        if not os.path.exists(video_file_path):
            download_video(video_path, video_file_path)
    else:
        video_file_path = video_path

    # frames_cache_file = os.path.join(cache_dir, f'{video_hash}_{num_frames}_frames.npy')
    # timestamps_cache_file = os.path.join(cache_dir, f'{video_hash}_{num_frames}_timestamps.npy')

    # if os.path.exists(frames_cache_file) and os.path.exists(timestamps_cache_file):
    #     log.info(f"Video frames already cached before")
    #     return video_file_path
    # try:
    #   vr = VideoReader(video_file_path, ctx=cpu(0))
    #   total_frames = len(vr)

    #   indices = np.linspace(0, total_frames - 1, num=num_frames, dtype=int)
    #   frames = vr.get_batch(indices).asnumpy()
    #   timestamps = np.array([vr.get_frame_timestamp(idx) for idx in indices])

    #   np.save(frames_cache_file, frames)
    #   np.save(timestamps_cache_file, timestamps)
    #   log.info(f"Video frames cached to {frames_cache_file} and {timestamps_cache_file}")
    # except Exception as e:
    #   log.exception(str(e))
    #   raise HTTPException(status_code=500, detail=str(e))
    return video_file_path