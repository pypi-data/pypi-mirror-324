from setuptools import setup, find_packages

setup(
    name="candleweb-ai",
    version="0.1.0",
    description="A custom tool for Candleweb AI Agents developers.",
    author="Candleweb Power Developers",
    author_email="ai@candleweb.com",
    url="https://github.com/edfolmi/candleweb-ai",
    packages=find_packages(),
    install_requires=[
        "crewai>=0.95.0",
        "pydantic>=1.10",  # Adjust version as necessary
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
