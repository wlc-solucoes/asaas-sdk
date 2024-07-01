from setuptools import (
    find_packages,
    setup
)

setup(
    name='asaas-sdk-wlc',
    packages=find_packages(include=['asaas']),
    version='0.1.3',
    license='Apache-2.0',
    description='SDK for Asaas API',
    author='WLC Soluções',
    author_email='fernando.leite@wlcsolucoes.com.br',
    url='https://github.com/wlc-solucoes/asaas-sdk/',
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.12',
    ]
)
