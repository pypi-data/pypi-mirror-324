# setup.py
from setuptools import setup, find_packages
import os

# 读取版本号
with open(os.path.join('md_dlp', '__init__.py'), 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'").strip('"')
            break

setup(
    name="md-dlp",
    version=version,
    author="MarkShawn",
    author_email="shawninjuly@gmail.com",
    description="A tool for markdown data loss prevention",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/markshawn2020/md-dlp",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'md-dlp=md_dlp.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
