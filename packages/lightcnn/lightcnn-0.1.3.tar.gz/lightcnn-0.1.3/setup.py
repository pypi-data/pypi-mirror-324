from setuptools import setup, find_packages

setup(
    name="lightcnn",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "opencv-python",
        "mtcnn",
        "tensorflow",
        "numpy",
        "scipy",
        "pillow"
    ],
    author="Yernar Bekbolat",
    author_email="dvayernar@gmail.com",
    description="LightCNN for fast, accurate and lightweight face verification",
    long_description="""
    # LightCNN

    Fast and accurate face recognition model optimized for Central Asian faces.

    ## GitHub
    For full documentation, examples, and source code:
    https://github.com/YernarBekbolat/LightCNN-V4-PyTorch
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "lightcnn": ["weights/*.pth.tar"],
    },
) 