#!/usr/bin/env python3

from setuptools import setup, find_packages

def get_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='captacity_clipify',
    version='0.3.4',
    packages=find_packages(),
    install_requires=get_requirements(),
    extras_require = {
        'local_whisper':  ["openai-whisper"],
    },
    package_data={
        'captacity_clipify': ['assets/**/*'],
    },
    include_package_data=True,
    url='https://github.com/adelelawady/captacity',
    license='MIT',
   author='Unconventional Coding',
    author_email='unconventionalcoding@gmail.com',
    description='Add Automatic Captions to YouTube Shorts with AI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'captacity=captacity.cli:main',
        ],
    },
)
