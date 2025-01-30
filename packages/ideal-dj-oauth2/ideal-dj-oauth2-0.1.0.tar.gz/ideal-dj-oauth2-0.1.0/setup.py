from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ideal-dj-oauth2",
    version="0.1.0",
    author="Prashant IdealITTechno",
    author_email="prashantidealittechno@gmail.com",
    description="A Django REST framework package for OAuth2.0 and social account management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prashantidealittechno/dj-oauth",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "Django>=3.0",
        "djangorestframework>=3.12",
        "requests>=2.25",
        "google-auth>=1.29",
        "pyjwt>=2.1",
    ],
)
