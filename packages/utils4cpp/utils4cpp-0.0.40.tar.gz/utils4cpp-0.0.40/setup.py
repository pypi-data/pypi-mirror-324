#!/usr/bin/env python
# coding: utf-8
from setuptools import find_packages, setup

setup(
    name="utils4cpp",
    version="0.0.40",
    packages=find_packages(),
    include_package_data=True,
    url="",
    license="MPL",
    author="last911",
    author_email="scnjl@qq.com",
    description="utils for cpp",
    install_requires=["sqlalchemy", "flask_sqlalchemy", "flask_sqlacodegen", "pymysql"],
)
