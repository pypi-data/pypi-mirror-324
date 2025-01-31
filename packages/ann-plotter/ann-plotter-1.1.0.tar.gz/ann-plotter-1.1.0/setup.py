from setuptools import setup, find_packages

setup(
    name="ann-plotter",
    version="1.1.0",
    author="Shivam Chaudhary",
    author_email="dragoonschaudhary@gmail.com",
    description="A package for visualizing artificial neural networks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shivamgithubok/ann-plotter",  # Ensure this is correct
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "networkx",
        "numpy",
        "plotly", 
        # "d3py"  # If you decide not to use it
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
