
from os         import environ
from setuptools import setup, find_packages


NL = '\n'

VERSION: str = environ.get('VERSION', '1.1.6')


with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()


setup(
    name=f'covvi-eci',
    version=VERSION,
    description='This project provides the ethernet interface to the COVVI Hand.',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    author='Jordan Birdsall',
    author_email='jordan.birdsall@covvi.com',
    maintainer='Jordan Birdsall',
    maintainer_email='jordan.birdsall@covvi.com',
    url='https://www.covvi-robotics.com/',
    classifiers=[line.strip() for line in '''
Operating System :: OS Independent
Programming Language :: Python :: 3.13
Programming Language :: Python :: 3.12
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.8
'''.strip().split(NL)],
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.8',
    package_data={
        'eci': ['py.typed'],
        'grips': ['*.gbc'],
    }
)
