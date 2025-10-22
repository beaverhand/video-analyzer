"""
Utility functions for working with NumPy arrays and .npy files.
"""
import numpy as np
from pathlib import Path
from typing import Union, Any, Optional

def load_npy(file_path: Union[str, Path]) -> np.ndarray:
    """
    Load a NumPy array from a .npy file.

    Args:
        file_path: Path to the .npy file

    Returns:
        np.ndarray: The loaded NumPy array

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not a valid .npy file
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if file_path.suffix != '.npy':
        raise ValueError(f"File must have .npy extension, got {file_path.suffix}")
    
    return np.load(str(file_path), allow_pickle=True)

def save_npy(array: np.ndarray, file_path: Union[str, Path]) -> None:
    """
    Save a NumPy array to a .npy file.

    Args:
        array: The NumPy array to save
        file_path: Path where to save the .npy file
    """
    file_path = Path(file_path)
    if file_path.suffix != '.npy':
        file_path = file_path.with_suffix('.npy')
    
    np.save(str(file_path), array)

def get_array_info(array: np.ndarray) -> dict:
    """
    Get information about a NumPy array.

    Args:
        array: The NumPy array to analyze

    Returns:
        dict: Dictionary containing array information
    """
    return {
        'shape': array.shape,
        'dtype': str(array.dtype),
        'min': float(np.min(array)) if array.size > 0 else None,
        'max': float(np.max(array)) if array.size > 0 else None,
        'mean': float(np.mean(array)) if array.size > 0 else None,
        'size': array.size,
        'nbytes': array.nbytes,
    }


if __name__ == "__main__":
  print(Path(".cache/d065bddf8616dd39cc8030177ac3ef21_128_frames.npy").exists())
  array = load_npy(".cache/d065bddf8616dd39cc8030177ac3ef21_128_frames.npy")
  metadata = load_npy(".cache/d065bddf8616dd39cc8030177ac3ef21_128_timestamps.npy")
  print(get_array_info(array))
  print("array: ", array[0].shape)
  print("metadata: ", metadata)