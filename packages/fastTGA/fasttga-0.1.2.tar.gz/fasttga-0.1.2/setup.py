from setuptools import setup, find_packages

setup(
    name='fastTGA',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'PyQt6',
        'gspread',
        'polars',
    ],
    author='Manuel Leuchtenmüller',
    author_email='manuel.leuchtenmueller@hydrogenreductionlab.com',
    description='A package for TGA data processing and management',
    url='https://github.com/yourusername/fastTGA',
)