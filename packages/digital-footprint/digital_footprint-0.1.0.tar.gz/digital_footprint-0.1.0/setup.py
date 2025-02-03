from setuptools import setup, find_packages

setup(
    name="digital_footprint",
    version="0.1.0",
    description="Digital Footprint Scanner: Free tool to extract useful information from an email.",
    author="ivanMartin",
    author_email="imartin.desarrollo@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "python-whois",
        "dnspython"
    ],
    entry_points={
        "console_scripts": [
            "digital_footprint = digital_footprint.scanner:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
