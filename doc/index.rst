.. Flask-Scss documentation master file, created by
   sphinx-quickstart on Fri Jul  8 17:32:32 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flask-Scss's documentation!
======================================



:Author:   `Bruno Carlin <http://bcarlin.net>`__
:Version:  |version|
:Date:     |today|
:Homepage: `Flask-Scss Homepage <http://packages.python.org/Flask-Scss>`__
:Download:  `Flask-Scss on PyPI <http://pypi.python.org/pypi/Flask-Scss>`__
:License:    MIT License
:Source code:  `Github project <https://github.com/bcarlin/flask-scss>`__
:Issue tracker:  `Github project <https://github.com/bcarlin/flask-scss>`__



.. contents::




This extension brings Scss support to Flask apps.

It is far from perfect or complete. Current features are the following:

- Automatic discovery of .scss assets
- Automatic compilation of .scss files
- Automatic refreshing of resulting .css files when .scss sources have changed
  (only if ``app.testing`` or ``app.debug`` are True)
- Configuration variables can be either set on the app config or given as an 
  option (it makes it easier to have different dev/test/prod settings)
- Graceful handling of partials
- Compatible with any scss framework (like Compass)
- Asset tree is kept when it is converted to css 
  (e.g: ``{assets}/foo/bar.scss`` will be compiled in ``{static}/foo/bar.css``)

Scss files compilation is done by the 
`pyScss <http://pypi.python.org/pypi/pyScss>`_ implementation by 
German M. Bravo (Kronuz). Refer to this package documentation to see the 
supported scss syntax.


Installation
------------

To install Flask-Scss, you can use ``pip``::

  pip install Flask-Scss

You can also checkout the development version ::

  git clone https://github.com/bcarlin/flask-scss.git

or using ``pip``::

  pip install git+https://github.com/bcarlin/flask-scss.git#egg=Flask-Scss-dev


Configuration
-------------

To get started all you need to do is to instanciate a Scss object after 
configuring the application::

  from flask import Flask
  from flask.ext.scss import Scss
  
  app = Flask(__name__)
  Scss(app)

.. warning::
   The import method has changed with Flask 0.8.
   If you used a previous version, please update your imports of Flask-Scss.
   The "old way will still work, but it is deprecated!

Flask-Scss will determine if it must refresh css files before each request by
looking at your application configuration. If ``app.testing`` or ``app.debug``
are True, it will refresh the .css file if the matching .scss file has been 
modified.

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

Configuration options
~~~~~~~~~~~~~~~~~~~~~

The following parameters are looked for first in the arguments given to the
:class:`Scss` class. if they are not found, they will be searched in the
application configuration (app.config).

+------------+-----------------+----------------------------------------------+
| static_dir | SCSS_STATIC_DIR | The path to the ``static`` directory of your |
|            |                 | application                                  |
+------------+-----------------+----------------------------------------------+
| asset_dir  | SCSS_ASSET_DIR  | The path to the ``assets`` directory where   |
|            |                 | Flask-Scss will search ``.scss`` files       |
+------------+-----------------+----------------------------------------------+
| load_paths | SCSS_LOAD_PATHS | A list of folders to add to pyScss load_paths|
|            |                 | (for ex., the path to a library like Compass)|
+------------+-----------------+----------------------------------------------+




.. _scss_discovery_rules: 

``.scss`` files discovery rules
-------------------------------

Flask-Scss will try to find the ``.scss`` files in an asset directory.
The ``asset`` directory will be selecting according to the following rules:

1. If ``asset_dir`` option is given to the class Scss:

   1. ``{asset_dir}/scss`` if this folder exists
   2. ``{asset_dir}`` if this folder exists

2. If ``app.config['SCSS_ASSET_DIR']`` option is is set on the application:

   1. ``{app.config['SCSS_ASSET_DIR']}/scss`` if this folder exists
   2. ``{app.config['SCSS_ASSET_DIR']}`` if this folder exists

3. If ``asset_dir`` option is NOT given to the class Scss and 
   ``app.config['SCSS_ASSET_DIR']`` is not set:

   1. ``{app.root_dir}/assets/scss`` if this folder exists
   2. ``{app.root_dir}/assets`` if this folder exists

If no asset directory is found, Flask-Scss will not be activated.


.. _static_discovery_rules: 

``static`` directory discovery rules
------------------------------------


Flask-Scss will put the ``.css`` files it generates in your ``static`` 
directory. The ``static`` directory will be resolved according to 
the following rules:

1. If ``static_dir`` option is given to the class Scss:

   1. ``{static_dir}``/css if this folder exists
   2. ``{static_dir}`` if this folder exists

2. If ``app.config['SCSS_STATIC_DIR']`` option is is set on the application:

   1. ``{app.config['SCSS_STATIC_DIR']}/css`` if this folder exists
   2. ``{app.config['SCSS_STATIC_DIR']}`` if this folder exists

3. If ``asset_dir`` option is NOT given to the class Scss and 
   ``app.config['SCSS_STATIC_DIR']`` is not set, Flask-Scss will
   build a "default" path from ``app.root_path`` and ``app.static_path``
   (``app`` is your Flask based application). following paths will then be
   tried:

   1. ``{default_static_dir}/css`` if this folder exists
   2. ``{default_static_dir}`` if this folder exists

If no static directory is found, Flask-Scss will not be activated.


Scss libraries search path
--------------------------

Scss frameworks like Compass heavily use ``@import`` directives.

You can specify the search path for such libraries by passing an extra argument
to :class:`Scss` ::
  
  Scss(app, load_paths=[
    '/Library/Ruby/Gems/1.8/gems/compass-0.11.5/frameworks/compass/stylesheets/'
  ])

or by setting an option in your app config::

  app.config['SCSS_LOAD_PATHS'] = [
    '/Library/Ruby/Gems/1.8/gems/compass-0.11.5/frameworks/compass/stylesheets/'
  ]


APIs
----

.. autoclass:: flaskext.flask_scss.Scss


Changes
-------

0.2 (2012/10/07)
~~~~~~~~~~~~~~~~
* Main enhancements and bugfixes:

  * New import scheme conforiming to Flask-0.8 ``flask.ext.*`` . 
    **The change is backward-compatible** (although deprecated!)
  * Asset tree is preserved during compilation to css
  * Asset dir is searched recursively (as it was expected!)
  * Do not compile scss files starting with an "_" anymore (they are considered 
    as partials)
  * Recompilation of all CSS files if a partial has been modified
  * Scss can be configured in app.config (it allows for different 
    dev/test/prod settings)
  * pyScss scss files search path can be configured by passing it to Scss() 
    or by adding an option to the app config
  * Looks for app.debug or app.testing to decide if it must automatically 
    refresh css before each requests or not

* Other internal changes:

  * migration to git and Github
  * Updates a lot of things to make the packages follow standard guidelines
  * Adds setup.cfg to automate doc build and upload
  * Moves tests out of the main package


0.1 (2011/07/08)
~~~~~~~~~~~~~~~~

* Initial release