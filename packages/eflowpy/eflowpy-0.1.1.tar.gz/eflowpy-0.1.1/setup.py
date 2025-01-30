from setuptools import setup, find_packages

# Read the README.md file as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="eflowpy",  # The name of your package
    version="0.1.1",  # Initial version
    description="A Python package for estimating environmental flow requirements using hydrological methods.",
    long_description=long_description,  # Add long description from README.md
    long_description_content_type="text/markdown",  # Specify markdown format
    author="Gokhan Cuceloglu",  # Replace with your name
    author_email="cuceloglugokhan@gmail.com",  # Replace with your email
    url="https://github.com/gokhancuceloglu/eflowpy",
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=["pandas", "numpy", "matplotlib", "scipy"],  # Add dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
)
