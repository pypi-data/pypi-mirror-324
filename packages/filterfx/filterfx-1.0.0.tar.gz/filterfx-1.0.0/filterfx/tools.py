import cv2 as cv
from cv2.typing import MatLike
from PIL.Image import Image
from PIL import Image as Img
import numpy as np

"""
This module provides utility functions for converting between OpenCV (cv2) image formats and Pillow (PIL) image formats, 
as well as ensuring that a given Pillow image is in RGB mode.
"""

def ensure_rgb(image: Image) -> Image:
    """Ensure that the image is in RGB mode."""
    if image.mode != "RGB":
        return image.convert("RGB")
    return image

def imageCV_to_imagePIL(cv_image: MatLike) -> Image:
    """Converts an OpenCV Image into a Pillow Image fortmat"""
    rbg_image = cv.cvtColor(cv_image, cv.COLOR_BGR2RGB)
    return Img.fromarray(rbg_image)

def imagePIL_to_imageCV(pillow_image: Image) -> MatLike:
    """Converts an Pillow Image into a OpenCV Image format"""
    cv_image = np.array(pillow_image)
    if pillow_image.mode == "RGB":
        return cv.cvtColor(cv_image, cv.COLOR_RGB2BGR)
    return cv_image

