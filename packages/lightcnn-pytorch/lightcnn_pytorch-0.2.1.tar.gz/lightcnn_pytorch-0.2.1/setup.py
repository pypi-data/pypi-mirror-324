from setuptools import setup, find_packages

setup(
    name="lightcnn-pytorch",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "numpy==2.2.2",
        "torch",
        "torchvision",
        "opencv-python",
        "facenet-pytorch",
        "scipy",
        "pillow",
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
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "lightcnn-pytorch": ["weights/*.pth.tar"],
    },
)
