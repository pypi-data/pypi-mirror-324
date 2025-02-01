from setuptools import setup, find_namespace_packages, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 1. Encuentra automáticamente los paquetes dentro de starlink_client
starlink_packages = find_namespace_packages(include=["starlink_client", "starlink_client.*"])

# 2. Encuentra los subpaquetes dentro de 'starlink_client/spacex' (por ejemplo: api, api.common, etc.)
#   - Usamos find_packages en lugar de find_namespace_packages porque 'spacex'
#     debe comportarse como un paquete "normal" con __init__.py.
spacex_subpackages = find_packages(where="starlink_client/spacex")

setup(
    name="starlink-client",
    version="0.1.9",
    # 3. Construimos la lista final de paquetes:
    #    - Los encontrados en starlink_client (paso 1).
    #    - El paquete top-level "spacex".
    #    - Sus subpaquetes "spacex.xxx"...
    packages=starlink_packages + ["spacex"] + ["spacex." + pkg for pkg in spacex_subpackages],

    # 4. Mapeamos la carpeta "starlink_client/spacex" al paquete top-level "spacex",
    #    y "starlink_client" a "starlink_client".
    package_dir={
        "starlink_client": "starlink_client",
        "spacex": "starlink_client/spacex",
    },

    include_package_data=True,
    package_data={
        "starlink_client": ["spacex/**"],  # Para que se incluyan los archivos generados
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
