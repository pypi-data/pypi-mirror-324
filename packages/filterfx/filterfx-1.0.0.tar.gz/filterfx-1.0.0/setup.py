from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Python package to enhance your images!'
LONG_DESCRIPTION = 'Python package to enhance and apply filters your images.'

setup(
        name="filterfx", 
        version=VERSION,
        author="Fabio Rojas",
        author_email="<fabiorrojas56@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'numpy>=2.2.2',
            'opencv-python>=4.11.0.86',
            'pillow>=11.1.0',
        ],
        
        keywords=['python', 'filters', 'image', 'enhance', 'pillow', 'opencv', 'ocr'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.12",
            "Operating System :: Microsoft :: Windows",
            "Topic :: Multimedia"
        ]
)