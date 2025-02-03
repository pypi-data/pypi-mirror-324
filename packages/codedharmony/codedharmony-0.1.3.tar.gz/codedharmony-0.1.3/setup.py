from setuptools import setup, find_packages

setup(
    name='codedharmony',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[],
    author='Andrew Vialichka',
    author_email='andreivialichka@onlineimmigrant.com',
    description='A collection of utility functions for harmonizing code.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/onlineimmigrant/codedharmony',  # replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
