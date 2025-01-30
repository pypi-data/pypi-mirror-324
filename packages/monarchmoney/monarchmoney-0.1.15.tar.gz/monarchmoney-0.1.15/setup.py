import os

from setuptools import setup

install_requires = open("requirements.txt", "r").read().split("\n")

setup(
    name="monarchmoney",
    description="Monarch Money API for Python",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hammem/monarchmoney",
    author="hammem",
    author_email="hammem@users.noreply.github.com",
    license="MIT",
    keywords="monarch money, financial, money, personal finance",
    install_requires=install_requires,
    packages=["monarchmoney"],
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Topic :: Office/Business :: Financial",
    ],
)
