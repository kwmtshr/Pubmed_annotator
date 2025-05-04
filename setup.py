# setup.py
from setuptools import setup, find_packages

setup(
    name="pubmed_client",
    version="0.1.0",
    description="Fetch and summarize PubMed abstracts with OpenAI",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "requests",
        "pandas",
        "python-dotenv",
        "tqdm",
        "openai",
        "ratelimit",
    ],
    entry_points={
        "console_scripts": [
            "run-pubmed=pubmed_client.cli:main"
        ]
    },
)
