from setuptools import setup, find_packages

# Read the README.md file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lmsystems',
    version='1.0.8',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'langgraph>=0.2.53',
        'langgraph_sdk>=0.1.36',
        'langchain-core>=0.3.31',
        'httpx>=0.24.0',
        'pyjwt>=2.0.0',
        'click>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'lmsystems=lmsystems.cli:cli',
        ],
    },
    author='Sean Sullivan',
    author_email='sean.sullivan3@yahoo.com',
    description='SDK for integrating purchased graphs from the lmsystems marketplace.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://docs.lmsystems.ai/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
