from PIL.Image import Image
import cv2 as cv

from typing import Union
from filterfx.tools import imagePIL_to_imageCV, imageCV_to_imagePIL

ImageType = Union[Image, cv.typing.MatLike]

def apply_ocr_from_path_opencv(
        image_path: str,
        has_dark_bg: bool = False,
        output: str = None, 
        show: bool = False,
    ) -> cv.typing.MatLike:

    try:
        image = cv.imread(image_path)

    except FileNotFoundError:
        raise FileNotFoundError(f"Image not found in path: {image_path}")
    
    except Exception as e:
        raise ValueError(f"Error opening image: {e}")

    return apply_ocr_filter(image, has_dark_bg, output, show)

def apply_ocr_filter(
        image: ImageType,
        has_dark_bg: bool = False,
        output: str = None,
        show: bool = False
    ) -> ImageType:

    if isinstance(image, Image):
        image = imagePIL_to_imageCV(image)

    ## ---- IMAGE PREPROCESSING ---- ##
    
    image = cv.GaussianBlur(image, (1,1), 0)
    
    #Identify character borders
    borders = cv.Laplacian(image, cv.CV_64F)
    borders = cv.convertScaleAbs(borders)
    borders = cv.bitwise_not(borders)

    # Fuse character borders with original image
    image = cv.addWeighted(image, 0.8, borders, 0.2, 0)
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    if has_dark_bg:
        image = cv.threshold(image, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    
    if show:
        cv.imshow("Image filtered for OCR", image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    if output:
        try:
            cv.imwrite(output, image)
            print(f"Image saved at: {output}")
        except IOError as e:
            raise IOError(f"Failed to save image to '{output}': {e}")

    if isinstance(image, Image):
        return imageCV_to_imagePIL(image)
    return image