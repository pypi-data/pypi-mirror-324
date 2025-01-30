from setuptools import setup, find_packages

setup(
    name="smartjoiner",
    version="1.0.0",
    author="Khalid Sulaiman Al-Mulaify",
    author_email="khalidmfy@gmail.com",
    description="A smart and flexible string joining library for Python developers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
)
