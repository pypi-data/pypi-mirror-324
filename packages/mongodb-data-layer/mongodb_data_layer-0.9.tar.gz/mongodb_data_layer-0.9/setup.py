from setuptools import setup, find_packages

setup(
    name='mongodb-data-layer',
    description='A data layer for mongodb',
    version='0.9',
    packages=find_packages(include=['mongodb_data_layer', 'mongodb_data_layer.*']),
    install_requires=[
        'pymongo',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'generate-model=mongodb_data_layer.generate_model:main'
        ]
    }
)