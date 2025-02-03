from setuptools import setup, find_packages

setup(
    name="scrapegen",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "langchain>=0.1.0",
        "langchain-google-genai>=0.0.1",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.7",
)