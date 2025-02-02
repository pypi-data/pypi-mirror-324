from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-intram",
    version="0.1.0",
    author="BAH SOUMANY Oualid",
    author_email="oualid.bahsoumany@suntech.bj",
    description="A Django plugin for Intram payment integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suntechdevs/django-intram.git",
    packages=find_packages(),
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
    ],
    python_requires=">=3.7",
    install_requires=[
        "Django>=3.2",
        "requests>=2.25.1",
    ],
)
