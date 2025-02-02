from setuptools import setup, find_packages

setup(
    name="printDelay",  
    version="0.1.1",  
    author="Mushfiq Shaikh",
    author_email="mushfiqshaikh2@gmail.com",
    description="A Python package for printing text with a delay effect.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Thiranium/printDelay",  
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)