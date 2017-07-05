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
        "toolz>=0.8.2",
        "pyserial>=3.3",
        "appJar>=0.6.1",
        "PyCmdMessenger>=0.2.4",
    ],
    python_requires='>=3.6',
    long_description=readme(),
    packages=["Robhat", "Robhat.Dome", "Robhat.Dome.UI", "Robhat.Dome.Control", "Robhat.Dome.Macros"],
    include_package_data=True,
)
