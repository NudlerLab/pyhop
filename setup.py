import os
from setuptools import find_packages, setup


def extract_version():
    """
    Extracts version values from the main matplotlib __init__.py and
    returns them as a dictionary.
    """
    with open('pyhop/__init__.py') as fd:
        for line in fd.readlines():
            if (line.startswith('__version__')):
                exec(line.strip())
    return locals()["__version__"]


def get_package_data():
    data = [
        'data/fastq/%s/*' % x
        for x in os.listdir('data/fastq')]

    return {
        'pyhop':
        data +
        [
            "notebooks/*.ipynb"
        ]}

setup(
    name="pyhop",
    version=extract_version(),
    author="Aviram Rasouly, Ilya Shamovsky",
    author_email="ilya.shamovsky@nyumc.org",
    url="https://github.com/eco32i/pyhop",
    license="MIT",
    packages=find_packages(),
    package_dir={"pyhop": "pyhop"},
    package_data=get_package_data(),
    description="TN-Seq anaylsis pipeline",
    # run pandoc --from=markdown --to=rst --output=README.rst README.md
    long_description=open("README.md").read(),
    # numpy is here to make installing easier... Needs to be at the
    # last position, as that's the first installed with
    # "python setup.py install"
    install_requires=["numpy",
                      "pandas"]
    entry_points={
        'console_scripts': [
# This is temporary
            'pyhop=pyhop.dmux:main',
            ],
        },
    classifiers=['Intended Audience :: Science/Research',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering :: Bio-Informatics',
                 'Topic :: Scientific/Engineering :: Visualization',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Operating System :: Unix',
                 'Operating System :: MacOS',
                 'Programming Language :: Python :: 3.5'],
    zip_safe=False)
