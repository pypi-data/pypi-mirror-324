from setuptools import setup, find_packages

setup(
    name='scrapyapi',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'fastapi-blueprint',
    ],
    entry_points={
        'console_scripts': [
            'scrapyapi=scrapyapi.app.main:app',
        ],
    },
)