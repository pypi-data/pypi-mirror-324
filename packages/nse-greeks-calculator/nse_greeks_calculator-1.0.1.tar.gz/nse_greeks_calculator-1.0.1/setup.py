from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nse-greeks-calculator",
    version="1.0.1",
    author="Lekshmi",
    description="A package for calculating option Greeks for NSE derivatives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=[
        "nsepython",
        "pandas",
        "numpy",
        "scipy"
    ],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    license="Apache-2.0",  # SPDX identifier
    include_package_data=True,
    # Explicitly prevent setuptools from auto-adding license-file
    license_files=[],  # Empty list disables auto-detection
)