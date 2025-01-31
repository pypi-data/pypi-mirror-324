from setuptools import setup, find_packages

setup(
    name="ann-plotter",
    version="1.0.0",
    author="Shivam Chaudhary",
    author_email="dragoonschaudhary@gmail.com",
    description="A package for visualizing artificial neural networks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shivamgithubok/ann_visualizer",  # Replace with your GitHub repo link
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "networkx",
        "numpy",
        "d3py"  # If required for visualization
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
