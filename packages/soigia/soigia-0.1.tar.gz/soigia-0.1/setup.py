import os
import re
import shutil
import sys
from io import open
from setuptools import find_packages, setup


def read(f):
    with open(f, "r", encoding="utf-8") as file:
        return file.read()


requirements = [
    "django>=4.2",
    "ccxt",
    "loguru",
    "pandas",
    "backtesting",
    "pydantic",
    "python-dotenv",
    "colorama",
    "python-binance",
    "python-box",
    "python-telegram-bot",
    "gspread",
    "oauth2client",
    "websocket-client",
    "typer",
    "ipython",
    "ipdb",
    "requests",
    "rich",
    "SqlAlchemy",
    "mysqlclient",
    "djangorestframework",
    "djangorestframework-simplejwt",
    "django-cors-headers",
    "drf-yasg",
    "drf-spectacular",
    "django-environ",
    "django-debug-toolbar",
]

setup(
    name="soigia",
    version="0.1",
    description="soigia python client for the official soigia API base on Django",
    long_description=read("README.pip.md"),
    long_description_content_type="text/markdown",
    author="soi gia",
    author_email="sojgja@gmail.com",
    # packages=find_packages(exclude=["tests*"]),
    packages=find_packages(include=["soigia", "soigia.*"]),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
