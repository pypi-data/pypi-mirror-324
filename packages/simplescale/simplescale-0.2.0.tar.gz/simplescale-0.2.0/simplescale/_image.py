"""_image module provides a wrapper around PIL.
"""

import dataclasses as dc
import numpy as np

def dimensions(image):
  if isinstance(image, np.ndarray):
    height, width = image.shape[:2]
    return width, height

  if hasattr(image, 'size'):
    return image.size[0], image.size[1]

  return None
