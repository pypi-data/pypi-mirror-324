from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name             = 'intermag',
    packages         = ['intermag'],
    version          = '0.0.2',
    description      = 'Python library to auto-download, manipulate, and process magnetic data from INTERMAGNET sites',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author           = 'Power_Broker',
    author_email     = 'gitstuff2@gmail.com',
    url              = 'https://github.com/PowerBroker2/intermag',
    download_url     = 'https://github.com/PowerBroker2/intermag/archive/0.0.2.tar.gz',
    keywords         = ['War Thunder'],
    classifiers      = [],
    install_requires = ['numpy', 'pandas', 'matplotlib', 'scipy', 'ppigrf']
)
