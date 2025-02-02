from setuptools import setup, find_packages

setup(
    name="cognilib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    author="Arman Maurya",
    author_email="armanmarya6@gmail.com",
    description="A machine learning library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/armanmaurya/learnix",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
