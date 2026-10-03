from setuptools import find_packages, setup

setup(
    name="enterprise-banking-data-platform",
    version="0.1.0",
    description="Synthetic enterprise banking data and analytics platform",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.26.0",
        "faker>=19.0.0",
        "pyyaml>=6.0",
        "fastapi>=0.110.0",
        "uvicorn>=0.29.0",
        "pydantic>=2.7.0",
        "pyarrow>=15.0.0",
    ],
)
