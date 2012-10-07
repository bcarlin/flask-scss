"""
Flask-scss
----------


This extension brings support for scss files to Flask. It uses `pyScss`_
compiler for scss files.

Links
`````

* `documentation <http://packages.python.org/Flask-Scss>`_
* `development version
  <https://github.com/bcarlin/flask-scss#egg=Flask-Scss-dev>`_

.. _pyScss: http://pypi.python.org/pypi/pyScss

"""
from setuptools import setup


setup(
    name='Flask-Scss',
    version='0.2',
    url='https://github.com/bcarlin/flask-scss',
    license='MIT',
    author='Bruno Carlin',
    author_email='bruno@bcarlin.net',
    description='Adds support for scss files to Flask applications',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask', 'pyScss'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
