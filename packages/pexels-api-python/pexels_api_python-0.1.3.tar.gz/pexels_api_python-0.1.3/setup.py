from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pexels_api_python",  # Name of your package
    version="0.1.3",           # Version number
    author="Harish Devathraj",        # Your name
    author_email="devathrajharish@gmail.com",  # Your email
    description="A Python wrapper for the Pexels API",  # Short description
    long_description=long_description,      # Long description from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/devathrajharish/pexels_api_python",  # Project URL
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=["requests"],  # Dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version required
)