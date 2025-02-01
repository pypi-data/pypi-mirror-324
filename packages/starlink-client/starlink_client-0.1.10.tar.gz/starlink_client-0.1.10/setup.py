from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="starlink-client",
    version="0.1.10",
    packages=find_packages(include=["starlink_client*", "spacex*"]),
    include_package_data=True,
    package_data={
        "spacex": ["**"],
        "starlink_client": ["**"],
    },
    install_requires=[
        "grpcio",
        "grpcio-status",
        "proto-plus",
        "protobuf",
        "requests",
        "httpx",
        "pydantic",
        "httpx[http2]",
    ],
    description="A Python client for Starlink.",
    author="Hector Oliveros",
    author_email="hector.oliveros.leon@gmail.com",
    url="https://github.com/Eitol/starlink-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires='>=3.9',
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="starlink client grpc satellite internet antenna",
)
