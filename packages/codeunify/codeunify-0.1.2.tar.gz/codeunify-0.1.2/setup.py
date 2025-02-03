from setuptools import setup, find_packages

# Read the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define the setup function
setup(
    name='codeunify',
    version='0.1.2',  # Update the version as per your release
    description='A library to combine multiple code files into one for easier AI context and error analysis',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specifies the format of the long description
    author='Phillip Chananda',  # Replace with your name
    author_email='takuphilchan@gmail.com',  # Replace with your GitHub username (email you use for GitHub)
    url='https://github.com/takuphilchan/codeunify',  # Replace with your GitHub repository URL
    packages=find_packages(),
    install_requires=[
        # List any dependencies your library requires, e.g., if logging, os, etc., are required, list them here
        'numpy',  # If numpy or any other package is a requirement
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Update according to the status of your library
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # You can adjust this if your code supports a different version of Python
    project_urls={
        "Bug Tracker": "https://github.com/takuphilchan/codeunify/issues",  # Update with your repository bug tracker link
        "Documentation": "https://github.com/takuphilchan/codeunify#readme",  # Link to your readme section or full docs
        "Source Code": "https://github.com/takuphilchan/codeunify",  # Link to the source code repository
    },
)
