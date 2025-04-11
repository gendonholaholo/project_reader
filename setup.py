from setuptools import setup, find_packages

setup(
    name="project-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.12.0",
        "python-dotenv>=1.0.0",
        "pathlib>=1.0.1",
        "typing-extensions>=4.9.0",
    ],
    entry_points={
        "console_scripts": [
            "project-analyzer=main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python project analyzer that generates comprehensive documentation using AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/project-analyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 