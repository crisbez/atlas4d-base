from setuptools import setup, find_packages

setup(
    name="atlas4d",
    version="0.1.0",
    description="Python client for Atlas4D API",
    author="Digicom Ltd",
    author_email="office@atlas4d.tech",
    url="https://github.com/crisbez/atlas4d-base",
    packages=find_packages(),
    install_requires=["requests>=2.25.0"],
    python_requires=">=3.8",
)
