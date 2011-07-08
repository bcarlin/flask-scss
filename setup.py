"""
Flask-scss
-------------

This extension brings support for scss files to Flask
"""
from setuptools import setup


setup(
    name='Flask-Scss',
    version='0.1',
    url='https://bitbucket.org/aerdhyl/flask-scss',
    license='MIT',
    author='Bruno Carlin',
    author_email='self@aerdhyl.eu',
    description='This extension brings support for scss files to Flask',
    long_description=open('README.txt').read(),
    packages=['flaskext', 'flaskext.test'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask', 'pyScss'
    ],
    classifiers=[
        'Development Status :: 4 - Beta'
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)