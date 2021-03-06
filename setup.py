from setuptools import setup, find_packages
from directus import __version__

setup(
    name="directus",    # Required
    version=__version__,    # Required
    description="Python software development kit for Directus client with functions for convenience",    # Required
    url="https://github.com/w3iw3i/directus-sdk",   # Optional
    author='',   # Optional
    classifiers=[   # Optional
        # How mature is this project? Common values are:
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",

        # Indicate who your project is intended for
        "Intended Audience :: Developers", "Topic :: Software Development :: Build Tools",

        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6"],
    packages=find_packages(exclude=["examples"]),   # Required
    install_requires=["requests"]
)