import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="drf-oauth2",
    version="0.2",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.0",
        "djangorestframework>=3.12",
        "google-api-core>=2.23.0"
    ],
    extras_require={
        "dev": ["black", "flake8", "pytest", "pytest-django"],  # Dasturlash muhitida tavsiya qilingan kutubxonalar
    },
    author="Jahongir Hakimjonov",
    author_email="jahongirhakimjonov@gmail.com",
    description="OAuth2 implementation for Django Rest Framework",
    keywords="django rest framework oauth2 authentication",
    url="https://github.com/JahongirHakimjonov/drf-oauth2",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)
