#!/usr/bin/env python
import setuptools

from django_classified import get_version  # noqa isort:skip

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    author='Sergey Lyapustin',
    name="django-classified",
    version=get_version().replace(' ', '-'),
    author_email="inoks@mail.ru",
    description="Django classified ads",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/inoks/django-classified",
    keywords='django classified ads',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        "django-bootstrap-form",
        "django-filter",
        "Django>=1.11,<2.1",
        "Pillow>=4.0",
        "sorl-thumbnail>=12",
        "unidecode",
        # Babel is used for currency formatting
        'Babel>=1.0,<3.0',
    ],
)
