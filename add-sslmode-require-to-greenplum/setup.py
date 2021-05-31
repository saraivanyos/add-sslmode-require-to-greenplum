try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='addsslmoderequiretogreenplum',
    version='0.1',
    author='Sara Ivanyos',
    author_email='ivanyoss@starschema.net',
    url='https://github.com/saraivanyos/add-sslmode-require-to-greenplum',
    packages=['addsslmoderequiretogreenplum'],
    license='MIT',
    description='A Python module for adding sslmode require to Tableau Greenplum data sources.'
    install_requires=[
        'tableauserverclient',
        'pandas',
        'numpy',
    ]
)
