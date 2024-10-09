from setuptools import setup, find_packages

setup(
    name='frontend',
    version='1.0.0',
    author='DCX/DT',
    description='The Backend for Cryptowatch',
    packages=find_packages(),
    entry_points={
        "console_scripts": ["cryptowatch = frontend.__main__:app"],
    },
)