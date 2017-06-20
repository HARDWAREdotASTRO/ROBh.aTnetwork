from setuptools import setup, find_packages
from typing import Text

def readme() -> Text:
    with open("README.md") as f:
        return f.read()

setup(
    name='Robhat',
    version='0.0.1',
    url='https://github.com/HARDWAREdotASTRO/ROBh.aTnetwork',
    license='MIT',
    author='Nick Meyer',
    author_email='nmeyer14@winona.edu',
    description='',
    install_requires=[
        "toolz",
        "pyserial",
        "appJar",
    ],
    python_requires='>=3.6',
    long_description=readme(),
    packages=["Robhat", "Robhat.Dome", "Robhat.Dome.UI", "Robhat.Dome.Serial"],
    include_package_data=True,
)
