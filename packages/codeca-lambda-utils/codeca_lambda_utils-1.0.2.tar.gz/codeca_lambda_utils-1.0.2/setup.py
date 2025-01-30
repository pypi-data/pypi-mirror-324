from setuptools import setup, find_packages

setup(
    name="Lambda Utils",
    version="0.1.0",
    description="Shared lambda utils for microservices",
    author="Kyle Hobeck",
    author_email="krhobeck@archdocs.dev",
    url="https://github.com/Codeca-Plus/lambda-utils",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)