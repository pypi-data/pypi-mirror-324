from setuptools import setup, find_packages

setup(
    name="Neuronn",
    version="0.1.0",
    author="Karthikeyan",
    author_email="karthikkrishna0907@gmail.com",
    description="A custum Python ML package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/neuron",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
