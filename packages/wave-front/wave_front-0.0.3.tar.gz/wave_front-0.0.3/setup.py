from setuptools import setup, find_packages

setup(
    name="wave_front",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        "h2o-wave==1.6.0",
    ],
)
