from setuptools import setup, find_packages

setup(
    name="ossbomer-schema",
    version="1.2.0",
    author="Oscar Valenzuela",
    author_email="oscar.valenzuela.b@gmail.com",
    description="OSSBOMER - SBOM Schema Validator for SPDX and CycloneDX",
    packages=find_packages(),
    install_requires=[
        "jsonschema",
        "xmlschema",
        "requests"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)
