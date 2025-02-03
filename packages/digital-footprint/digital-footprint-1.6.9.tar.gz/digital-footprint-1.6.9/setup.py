from setuptools import setup, find_packages

setup(
    name="digital-footprint",
    version="1.6.9",
    description="Digital Footprint Scanner: Free tool to extract useful information from an email.",
    author="IvanMartin",
    author_email="imartin.desarrollo@gmail.com",
    packages=find_packages(),
    install_requires=[
    "requests",
    "python-whois",
    "dnspython",
    "waybackpy",
    "colorama",
    "googlesearch-python"
    ],
    entry_points={
    "console_scripts": [
        "digital-footprint = digital_footprint.scanner:main"
    ]
},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
