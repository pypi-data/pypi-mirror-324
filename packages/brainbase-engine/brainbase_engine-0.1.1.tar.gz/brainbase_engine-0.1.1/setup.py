from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="brainbase-engine",
    version="0.1.1",
    author="Brainbase Labs",
    author_email="	support@usebrainbase.xyz",
    description="Official Python SDK for Brainbase's REST & WebSocket API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brainbase/brainbase-python",
    project_urls={
        "Bug Tracker": "https://github.com/brainbase/brainbase-python/issues",
        "Documentation": "https://docs.brainbase.com/python",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "websocket-client>=1.0.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "isort>=5.0",
            "mypy>=0.900",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
)
