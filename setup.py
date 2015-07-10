"""
Flask-scss
"""
from setuptools import setup
import os

with open('README.rst') as readme:
    LONG_DOC = readme.read()


def make_data_files(root_path, base_target):
    ret = []
    tmp = []
    for elem in os.listdir(root_path):
        full_path = os.path.join(root_path, elem)
        if os.path.isfile(full_path):
            tmp.append(full_path)
        else:
            ret += make_data_files(full_path, os.path.join(base_target, elem))
    ret.append((base_target, tmp))
    return ret

setup(
    name='Flask-Scss',
    version='0.4',
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
    data_files=make_data_files('doc/.build/html', 'doc') + [
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
