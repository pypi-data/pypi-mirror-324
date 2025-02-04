from setuptools import setup, find_packages

setup(
    name="souravroy0407",
    version="0.6",
    author="souravroy0407",
    description="A simple package with a hello function",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        "console_scripts":[
            "sourav0407 = sourav0407:hello"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", 
    ],
      
)
