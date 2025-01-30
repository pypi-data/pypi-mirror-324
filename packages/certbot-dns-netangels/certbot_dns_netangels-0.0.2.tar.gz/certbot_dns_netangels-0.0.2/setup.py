from os import path
from setuptools import setup, find_packages

version = "0.0.2"
install_requires = [
    "acme>=0.29.0",
    "certbot>=0.34.0",
    "setuptools",
    "requests",
    "tldextract",
    "mock",
    "requests-mock",
]

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="certbot-dns-netangels",
    version=version,
    description="netangels DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/navigatore300/certbot-dns-netangels",
    author="Maksimov Denis",
    author_email="maximden@mail.ru",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "certbot.plugins": [
            "dns-netangels = certbot_dns_netangels.dns_netangels:Authenticator"
        ]
    },
)
