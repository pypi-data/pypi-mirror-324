from setuptools import setup, find_packages

setup(
    name="NXDB",
    version="0.1.0.1",
    packages=find_packages(),
    install_requires=["pyyaml"],
    author="VladosNX",
    author_email="email.name@email.com"
)

# Run `python3 setup.py sdist bdist_wheel`
