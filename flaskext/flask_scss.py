from __future__ import with_statement
import os.path as op
import os
import scss


class Scss(object):
    '''
    Main and only class for Flask-Scss. It is in charge on the discovery of
    .scss files and compiles them every time they are modified.
    
    Any application that wants to use Flask-Scss must create a instance of this class
    '''
    
    def __init__(self, app, static_dir=None, asset_dir=None):
        '''
        
        See :ref:`scss_discovery_rules` 
        and :ref:`static_discovery_rules`
        for more information about the impact of ``static_dir`` and  
        ``asset_dir`` parameters.
        
        :param app: Your Flask Application
        :param static_dir: The path to the ``static`` directory of your 
                           application (optionnal)
        :param asset_dir: The path to the ``assets`` directory where Flask-Scss
                          will search ``.scss`` files (optionnal)
        '''
        self.app = app
        self.asset_dir = self.set_asset_dir(asset_dir)
        self.static_dir = self.set_static_dir(static_dir)
        self.assets = {}
        self.compiler = scss.Scss().compile
        self.set_hooks()

    def set_asset_dir(self, asset_dir):
        asset_dir = asset_dir if asset_dir is not None \
                        else op.join(self.app.root_path, 'assets')
        if op.exists(op.join(asset_dir, 'scss')):
            return op.join(asset_dir, 'scss')
        if op.exists(asset_dir):
            return asset_dir
        return None

    def set_static_dir(self, static_dir):
        static_dir = static_dir if static_dir is not None \
                       else op.join(self.app.root_path, self.app.static_folder)
        if op.exists(op.join(static_dir, 'css')):
            return op.join(static_dir, 'css')
        if op.exists(static_dir):
            return static_dir
        return None

    def set_hooks(self):
        if self.asset_dir is None:
            self.app.logger.warning("The asset directory cannot be found."
                                    "Flask-Scss extension has been disabled")
            return
        if self.static_dir is None:
            self.app.logger.warning("The static directory cannot be found."
                                    "Flask-Scss extension has been disabled")
            return
        self.app.logger.info("Pyscss loaded!")
        self.app.before_request(self.update_scss)

    def discover_scss(self):
        for filename in (f for f in os.listdir(self.asset_dir)
                         if f.endswith('.scss')):
            if filename not in self.assets:
                src_path = op.join(self.asset_dir, filename)
                dest_path = op.join(self.static_dir,
                                    filename.replace('.scss', '.css'))
                self.assets[filename] = {'src_path': src_path,
                                         'dest_path': dest_path}

    def update_scss(self):
        self.discover_scss()
        for asset in self.assets.values():
            dest_mtime = op.getmtime(asset['dest_path']) \
                             if op.exists(asset['dest_path']) \
                             else -1
            if op.getmtime(asset['src_path']) > dest_mtime:
                self.compile_scss(asset)

    def compile_scss(self, asset):
        self.app.logger.info("[flask-pyscss] refreshing %s" \
                                % (asset['dest_path'],))
        with open(asset['dest_path'], 'w') as fo:
            with open(asset['src_path']) as fi:
                fo.write(self.compiler(fi.read()))
