from setuptools import setup, find_packages
from typing import Text


def readme() -> Text:
    with open("README.md") as f:
        return f.read()

if __name__=="__main__":
    setup(
        name='Robhat',
        version='0.1.0',
        url='https://github.com/HARDWAREdotASTRO/ROBh.aTnetwork',
        license='MIT',
        author='Nick Meyer',
        author_email='nmeyer14@winona.edu',
        description='',
        platforms=['Unix'],
        install_requires=[
            "toolz>=0.8.2",
            "pyserial>=3.3",
            "appJar>=0.6.1",
            "PyCmdMessenger>=0.2.4",
            "numpy>=1.13.1",
            "scipy>=0.19.0",
            "smbus2>=0.1.5",
            "fake_rpi>=0.3.1",
        ],
        extras_require={
            'dev': [
                'sphinx>=1.6.3', 
                'recommonmark>=0.4.0',
                'sphinx_bootstrap_theme>=0.5.3',
                'sphinx-autobuild>=0.6.0'
                ]
        },                
        python_requires='>=3.6',
        # long_description=readme(),
        include_package_data=True,
    )
