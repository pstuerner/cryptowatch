from setuptools import setup, find_packages

setup(
    name='backend',
    version='1.0.0',
    author='DCX/DT',
    description='The Backend for Cryptowatch',
    packages=find_packages(),
    entry_points={
        "console_scripts": ["cryptowatch = backend.__main__:app"],
    },
)