from setuptools import setup, find_packages

setup(
    name="codecs_protocol",
    version="1.0.2", 
    author="Chandan Sharma",
    author_email="chandansharma7012@gmail.com",
    description="A Python library for decoding AVL packets (Codec8 & Codec8E).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
