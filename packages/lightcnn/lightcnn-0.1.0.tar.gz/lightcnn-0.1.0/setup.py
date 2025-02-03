from setuptools import setup, find_packages

setup(
    name="lightcnn",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "opencv-python",
        "mtcnn",
        "numpy",
        "scipy",
        "pillow"
    ],
    author="Yernar Bekbolat",
    author_email="dvayernar@gmail.com",
    description="LightCNN for face verification",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YernarBekbolat/LightCNN-V4-PyTorch",
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