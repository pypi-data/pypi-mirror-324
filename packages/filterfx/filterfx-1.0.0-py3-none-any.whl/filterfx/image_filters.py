from PIL import Image as Img
from PIL import ImageOps
from PIL.Image import Image
from enum import Enum
from filterfx.image_enhances import enhance_blur, enhance_color, enhance_contrast, add_noise
from filterfx.tools import ensure_rgb

class FILTER(Enum):
    SEPIA = "sepia"
    GRAYSCALE = "grayscale"
    INVERT = "invert"
    VINTAGE = "vintage"

AVAILABLE_FILTERS = FILTER._member_names_

def get_filters() -> None:
    print(AVAILABLE_FILTERS)

def _apply_sepia(image: Image) -> Image:
    """ Apply the sepia filter to an image"""
    sepia = Img.new("RGB", image.size)
    px = image.load()
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = px[x, y]
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            sepia.putpixel((x, y), (min(tr, 255), min(tg, 255), min(tb, 255)))
    return sepia

def _apply_invert(image: Image) -> Image:
    """Inverts the color to an image"""
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    inverted_image = ImageOps.invert(image)
    return inverted_image

def _apply_vintage(image: Image) -> Image:
    """ Apply the vintage filter to an image"""
    vintage = _apply_sepia(image)
    
    vintage = enhance_color(vintage, 0.8)
    vintage = enhance_contrast(vintage, 1.2)
    vintage = enhance_blur(vintage, 1.2)
    vintage = add_noise(vintage, 17)

    return vintage

FILTER_FUNCTIONS = {
    FILTER.SEPIA: _apply_sepia,
    FILTER.GRAYSCALE: lambda img: img.convert("L"),
    FILTER.INVERT: _apply_invert,
    FILTER.VINTAGE: _apply_vintage,
}

def apply_filter_from_path(image_path: str, filter: FILTER, output: str = None, show: bool = False) -> Image:
    """
    Apply a filter to an image given by a valid path.

    Parameters
    ----------
    
    image_path: str
        Valid file path to an image.

    filter: FILTER
        Filter to apply (e.g., FILTER.SEPIA, FILTER.GRAYSCALE ).To see all filters use: 
        >>> get_filters()

    output: str, optional
        File path to save the filtered image, If None, the filtered image will be not saved.
        Defaults to None
    
    show: bool, optional
        Whether to display the image after applying the filter. Defaults to False

    Returns
    -------
    PIL.Image.Image
        The filtered image object (Pillow Image)

    Raises
    ------

    FileNotFoundError
        If the file at `image_path` does not exist.
    
    ValueError
        If there is an error loading the image or the filter is invalid.

    Examples
    --------

    Apply a grayscale filter to an image and save it:

    >>> apply_filter(imageObject, FILTER.GRAYSCALE, output="output.jpg")

    Apply a sepia filter to an image and display the result without saving:
    
    >>> apply_filter(imageObject, FILTER.SEPIA, show=True)
    
    """
    try:
        img = Img.open(image_path)

    except FileNotFoundError:
        raise FileNotFoundError(f"Image not found in path: {image_path}")
    
    except Exception as e:
        raise ValueError(f"Error opening image: {e}")

    return apply_filter(img, filter, output, show)

def apply_filter(image: Image, filter: FILTER, output: str = None, show: bool = False) -> Image:
    """
    Apply a filter to an image given by a valid path.

    Parameters
    -----------
    
    image: PIL.Image.Image
        Pillow Image Object.

    filter: FILTER
        Filter to apply (e.g., FILTER.SEPIA, FILTER.GRAYSCALE ).To see all filters use: 
        >>> get_filters()
    
    output: str, optional
        File path to save the filtered image, If None, the filtered image will be not saved.
        Defaults to None.
    
    show: bool, optional
        Whether to display the image after applying the filter. Defaults to False.

    Returns
    --------
    PIL.Image.Image
        The filtered image object (Pillow Image).

    Raises
    ------
    ValueError
        If `filter` is invalid.
    
    IOError
        If there is an error saving the image at `output` path.

    Examples
    --------

    Apply a grayscale filter to an image and save it:

    >>> apply_filter_from_path("example.jpg", FILTER.GRAYSCALE, output="output.jpg")

    Apply a sepia filter to an image and display the result without saving:
    
    >>> apply_filter_from_path("example.jpg", FILTER.SEPIA, show=True)
    
    """
    image = ensure_rgb(image)

    if filter not in FILTER_FUNCTIONS:
            raise ValueError(f"Filter {filter.name} not found")
    
    image = FILTER_FUNCTIONS[filter](image) #Executes the function according filter.

    if output:
        try:
            image.save(output)
            print(f"Image saved at: {output}")
        except IOError as e:
            raise IOError(f"Failed to save image to '{output}': {e}")
        
    if show:
        image.show()

    return image