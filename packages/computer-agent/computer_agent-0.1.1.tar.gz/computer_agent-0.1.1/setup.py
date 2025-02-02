from setuptools import setup, find_packages

setup(
    name="computer-agent",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "anthropic>=0.19.0",
        "jsonschema==4.22.0",
        "fastapi>=0.115.0",
        "uvicorn>=0.15.0",
        "sse-starlette>=1.0.0"
    ],
    author="b",
    author_email="bb@fea.st",
    description="Giving Agents Computers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
) 