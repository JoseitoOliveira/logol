import json

from setuptools import setup, find_packages

setup(
    name='logol',
    version=json.load(open('pkg_info.json'))['__version__'],
    author=['Joseíto Oliveira'],
    python_requires='>3.8',
    url='https://github.com/JoseitoOliveira/logol',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ]
)
