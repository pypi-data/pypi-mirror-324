from setuptools import setup, find_packages
import configparser

# Read the version from setup.cfg
config = configparser.ConfigParser()
config.read('setup.cfg')
version = config['bumpversion']['current_version']

setup(
    name='equator_qa',
    version=version,
    packages=find_packages(),
    install_requires=[
        "numpy>=1.18.0",
        "requests>=2.25.0",
        "jupyter",
        # Add other runtime dependencies here
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-mock",
            "flake8",
            "twine",
            "bump2version",
            "datasets",
            # Add other development dependencies here
        ],
    },
    entry_points={
        "console_scripts": [
            "equator = equator_qa.main:main",
        ],
    },
    package_data={
        "equator_qa": [
            "data/*",
            "assets/*",
            "images/*",
            "docs/*",
            "tests/*",
            "docbooks/*",
            "html/*",
            "latex/*"
        ],
    },
    # Additional metadata
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your package",
    url="https://github.com/raymondbernard/equator-qa",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
