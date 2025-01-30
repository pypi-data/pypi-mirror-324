from setuptools import setup, find_packages

setup(
    name="simplex",
    version="1.2.9",
    packages=find_packages(),
    package_data={
        "simplex": ["browser_agent/dom/*.js"],  # Include JS files in the dom directory
    },
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "tiktoken>=0.5.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "playwright>=1.0.0",
        "Pillow>=9.0.0",
        "PyYAML>=6.0.1",
        "boto3>=1.28.0",
        "requests>=2.31.0",
        "MainContentExtractor",
        "langchain_core",
        "langchain_community",
        "langchain_openai",
        "langchain_anthropic"
    ],
    entry_points={
        'console_scripts': [
            'simplex=simplex.cli:main',
        ],
    },
    author="Simplex Labs, Inc.",
    author_email="founders@simplex.sh",
    description="Official Python SDK for Simplex API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://simplex.sh",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.9",
) 