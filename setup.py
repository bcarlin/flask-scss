"""
Flask-scss
"""
from setuptools import setup
import os

with open('README.rst') as readme:
    LONG_DOC = readme.read()


setup(
    name='Flask-Scss',
    version='0.5',
    url='https://github.com/bcarlin/flask-scss',
    license='MIT',
    author='Bruno Carlin',
    author_email='bruno@bcarlin.net',
    description='Adds support for scss files to Flask applications',
    long_description=LONG_DOC,
    py_modules=['flask_scss'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask', 'pyScss'
    ],
    data_files=[
        ('.', ['tox.ini', 'LICENSE.txt', 'README.rst', 'AUTHORS']),
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
