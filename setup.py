#!/usr/bin/env python
import setuptools

from django_classified import get_version  # noqa isort:skip

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    author="Sergey Lyapustin",
    name="django-classified",
    version=get_version().replace(" ", "-"),
    author_email="s.lyapustin@gmail.com",
    description="Django Classified",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slyapustin/django-classified",
    keywords="django classified",
    packages=setuptools.find_packages(exclude=("demo",)),
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "django-bootstrap-form",
        "django-filter",
        "Django>=4.2,<5.2",
        "Pillow",
        "sorl-thumbnail",
        "unidecode",
        # Babel is used for currency formatting
        "babel",
    ],
)
