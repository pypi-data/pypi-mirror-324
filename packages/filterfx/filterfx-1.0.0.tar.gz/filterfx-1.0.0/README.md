# FilterFX
FilterFX is a Python package that allows users and developers to enhance images by applying a variety of filters easily.

## 🚀 **Getting Started** 

### ✅ Prerequisites  
Before installing, ensure you have the following:  
- Python **3.12.8** or later installed.  
- A virtual environment is recommended.

### Installation
To install FilterFX, simply run:  

```sh
pip install filterfx
```

## 🖼️ **Usage**
First, import the package:

```python
import filterfx as ffx
```

### 📌 **Applying Filters**
You can apply filters using either a PIL image object or directly from an image path.

#### 🖼️ Using a PIL Image object

```python
from PIL import Image

image = Image.new("path/to/your/image.jpg")
image = ffx.apply_filter(image, ffx.FILTERS.SEPIA)
image.show()
```
#### 📂 Using an image file path

```python
image = ffx.apply_filter_from_path("path/to/your/image2", ffx.FILTERS.GRAYSCALE)
```
### 💾 Saving & Displaying Results
You can save the processed image or display it in a window:

```python
#Save the filtered image
image = Image.new("path/to/your/image")
image = ffx.apply_filter(image, ffx.FILTERS.SEPIA, output="path/to/save/image")

#Show the filtered image in a new window
image = ffx.apply_filter_from_path("path/to/your/image2", ffx.FILTERS.GRAYSCALE, show=True)
```

### 🎨 Available Filters


| Filter Name   | Description     |
|---------------|-----------------|
| `ffx.FILTERS.SEPIA`      | Applies a warm, brownish tone to create an old-fashioned look. |
| `ffx.FILTERS.GRAYSCALE`  | Converts the image into a monochrome black & white style. |
| `ffx.FILTERS.INVERT`     | Reverses the colors, creating a negative effect. |
| `ffx.FILTERS.VINTAGE`    | Adds a retro-style filter with faded colors and soft contrast. |


## 📌 Example Results
**ORIGINAL IMAGE**

![original_image](/docs/images/example.jpg)

**SEPIA FILTER**

![sepia_filter](/docs/images/sepia.jpg)

**GRAYSCALE FILTER**

![sepia_filter](/docs/images/grayscale.jpg)


## 📂 More Examples

For additional examples, check out ![examples/example.py](https://github.com/SymbiontZ/filterfx/blob/main/examples/example.py).

## 📜 License
FilterFX is released under the MIT License.

## 👨‍💻 Credits & Contributions

### 🎨 Developed by  
- [Fabio Rojas](https://github.com/symbiontz) - Creator

### 📦 Dependencies 
- [Pillow](https://python-pillow.org/) - Image processing library  
- [NumPy](https://numpy.org/) - Used for efficient matrix operations


The images used in this project are from the game *Milk outside a bag of milk outside a bag of milk*, developed by [Nikita Kryukov](https://store.steampowered.com/app/1604000/Milk_outside_a_bag_of_milk_outside_a_bag_of_milk/).  
All rights belong to their respective owners.

