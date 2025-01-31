from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'mongodb_data_layer/README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='mongodb-data-layer',
    description='A data layer for mongodb',
    version='1.0',
    packages=find_packages(include=['mongodb_data_layer', 'mongodb_data_layer.*']),
    install_requires=[
        'pymongo',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'generate-model=mongodb_data_layer.generate_model:main'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)