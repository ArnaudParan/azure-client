from distutils.core import setup

setup(
    name = "azure_client",
    packages = ["azure_client"],
    version = "1.0.9",
    description = "Library which handles the microsoft Azure REST API",
    author = "Arnaud Paran",
    author_email = "paran.arnaud@gmail.com",
    url = "https://github.com/ArnaudParan/azure-client",
    download_url = "https://github.com/ArnaudParan/azure-client/archive/master.zip",
    keywords = ["microsoft", "azure"],
    install_requires = ['selenium'],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",  # TODO choose
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = "")
