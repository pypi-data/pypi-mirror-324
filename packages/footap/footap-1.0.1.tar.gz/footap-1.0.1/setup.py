from setuptools import setup, find_packages

setup(
    name="footap",
    version="1.0.1",
    author="Dims",
    description="Package de détection et suivi de jonglage de football",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "opencv-contrib-python>=4.5.0",
        "mediapipe>=0.8.0",
        "numpy>=1.19.0",
        "ultralytics>=8.0.0",
        "Pillow>=8.0.0"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video :: Capture",
    ],
)
