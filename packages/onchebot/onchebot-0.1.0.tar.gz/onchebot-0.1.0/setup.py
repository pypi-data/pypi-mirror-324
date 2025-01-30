from setuptools import find_packages, setup

setup(
    name="onchebot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp==3.9.3",
        "aiolimiter==1.1.0",
        "redis==5.2.1",
        "types-redis==4.6.0.20241004",
        "async_timeout==5.0.1",
        "beautifulsoup4==4.12.3",
        "dacite==1.8.1",
        "pytest==7.4.4",
        "pytest-mock==3.14.0",
        "pytest-asyncio==0.23.6",
        "fakeredis==2.26.2",
        "googletrans==4.0.2",
        "apscheduler==3.11.0",
        "python-logging-loki==0.3.1",
        "prometheus-client==0.21.0",
    ],
    author="Pepe",
    python_requires=">=3.11",
    include_package_data=True,
    zip_safe=False,
)
