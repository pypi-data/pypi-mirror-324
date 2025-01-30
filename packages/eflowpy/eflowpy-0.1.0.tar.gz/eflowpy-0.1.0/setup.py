from setuptools import setup, find_packages

setup(
    name="eflowpy",  # The name of your package
    version="0.1.0",  # Initial version
    description="A Python package for estimating environmental flow requirements using hydrological methods.",
    author="Gokhan Cuceloglu",  # Replace with your name
    author_email="cuceloglugokhan@gmail.com",  # Replace with your email
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=["pandas", "numpy", "matplotlib", "scipy"],  # Add dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
)
