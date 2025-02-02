from setuptools import setup, find_packages

setup(
    name="downloadYTscript",
    version="0.1.0",
    author="ehzawad",
    author_email="ehzawad@gmail.com",
    description="A command-line tool to download YouTube transcripts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "youtube-transcript-api>=0.4.0",
    ],
    entry_points={
        'console_scripts': [
            'downloadYTscript = downloadyt.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

