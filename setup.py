from setuptools import (
    find_packages,
    setup
)

setup(
    name='asaas-sdk-wlc',
    packages=find_packages(include=['asaas']),
    version='0.1.0',
    description='SDK for Asaas API',
    author='WLC Soluções',
    install_requires=['requests'], 
)