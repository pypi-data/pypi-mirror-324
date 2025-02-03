from setuptools import find_packages, setup

setup(
    name='ocean_qap',
    packages=find_packages(include=['ocean_qap']),
    version='0.0.2',
    description='Prototype library for solving QAP with the Ocean SDK',
    author='Atharv Chowdhary',
    install_requires=[
        "matplotlib>=3.0.0",
        "numpy>=1.19.0",
        "networkx>=2.5",
        "dwave-ocean-sdk>=5.5.0"
    ]
)
