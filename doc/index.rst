.. Flask-Scss documentation master file, created by
   sphinx-quickstart on Fri Jul  8 17:32:32 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flask-Scss's documentation!
======================================


.. contents::


This extension brings Scss support to Flask apps.

It is far from perfect or complete. Current features are the following:

- Automatic discovery of .scss assets
- Automatic compilation of .scss files
- Automatic refreshing of resulting .css files when .scss sources have changed

Scss files compilation is done by the 
`pyScss <http://pypi.python.org/pypi/pyScss>`_ implementation by 
German M. Bravo (Kronuz). Refer to this package documentation to see the 
supported scss syntax.


Installation
------------

To install Flask-Scss, you can use ``pip``::

  pip install Flask-Scss

You can also checkout the development version ::

  hg clone https://aerdhyl@bitbucket.org/aerdhyl/flask-scss

or using ``pip``::

  pip install hg+https://bitbucket.org/aerdhyl/flask-scss#egg=Flask-Scss-dev


Configuration
-------------

To get started all you need to do is to instanciate a Scss object after 
configuring the application::

  from flask import Flask
  from flaskext.flask_scss import Scss
  
  app = Flask(__name__)
  Scss(app)

Flask-Scss will now check before each request wether a .scss file has been 
modified. If so, it will refresh the corresponding .css file. To avoid the 
overhead of CSS refreshing, you can limit live scss refreshing to the 
development server::

  from flask import Flask
  from flaskext.flask_scss import Scss
  
  app = Flask(__name__)

  # ... your code ...

  if __name__ == '__main__':
    Scss(app)
    app.run()

You will then have to generate css files yourself for other setups 
(WSGI server, etc...)

For each .scss file found in the "asset" directory, a corresponding .css file 
will be created. 

The class ``Scss`` can take two additionnal optionnal parameters:

- ``asset_dir``: specifies the directory where to look for ``.scss`` files
- ``static_dir``: specifies the directory where to put generated ``.css`` files

For example, calling::
  
  Scss(app, static_dir='static', asset_dir='assets')

will expect the following layout::

  flask_app_root/
    static/
    assets/
      scss/
    ...other files...

.. _scss_discovery_rules: 

``.scss`` files discovery rules
-------------------------------

Flask-Scss will try to find the ``.scss`` files in an asset directory.
The ``asset`` directory will be selecting according to the following rules:

1. If ``asset_dir`` option is given to the class Scss:

   1.1. ``{asset_dir}/scss`` if this folder exists
   1.2. ``{asset_dir}`` if this folder exists

2. If ``asset_dir`` option is NOT given to the class Scss (``app`` is your Flask 
   based application):

   2.1. ``{app.root_dir}/assets/scss`` if this folder exists
   2.2. ``{app.root_dir}/assets`` if this folder exists

If no asset directory is found, Flask-Scss will not be activated.


.. _static_discovery_rules: 

``static`` directory discovery rules
------------------------------------


Flask-Scss will put the ``.css`` files it generates in your ``static`` 
directory. The ``static`` directory will be resolved according to 
the following rules:

1. If ``static_dir`` option is given to the class Scss:

   1.1. ``{static_dir}``/css if this folder exists
   1.2. ``{static_dir}`` if this folder exists

2. If ``static_dir`` option is NOT given to the class Scss, Flask-Scss will
   build a "default" path from ``app.root_path`` and ``app.static_path``
   (``app`` is your Flask based application). following paths will then be
   tried:

   2.1. ``{default_static_dir}/css`` if this folder exists
   2.2. ``{default_static_dir}`` if this folder exists

If no static directory is found, Flask-Scss will not be activated.

APIs
----

.. autoclass:: flaskext.flask_scss.Scss

