# setup.py
from setuptools import setup, find_packages

setup(
    name="md-dlp",
    version="0.2.0",
    author="MarkShawn",
    author_email="shawninjuly@gmail.com",
    description="A tool for markdown data loss prevention",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/markshawn2020/md-dlp",
    packages=find_packages(),
    py_modules=["md_dlp"],
    install_requires=[
        "requests>=2.25.1",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'md-dlp=md_dlp:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
