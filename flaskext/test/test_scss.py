from __future__ import with_statement
try:
    import unittest2 as unittest
except ImportError:
    import unittest # NOQA
import os
import os.path as op
import shutil
from mock import Mock
from flask import Flask
import flaskext.flask_scss
import time

SCSS_CONTENT = "a { color: red; text-decoration: none; }"


class ScssTest(unittest.TestCase):

    def setUp(self):
        self.test_data = op.join(os.getcwd(), 'test_data')
        os.makedirs(self.test_data)
        self.app = Mock()
        self.app.root_path = self.test_data
        self.app.static_folder = op.join(self.test_data, 'static')

    def tearDown(self):
        shutil.rmtree(self.test_data, ignore_errors=True)

    def set_layout(self, base=None):
        base = base if base is not None else self.test_data
        self.static_dir = op.join(base, 'static')
        os.makedirs(self.static_dir)
        self.asset_dir = op.join(base, 'assets')
        os.makedirs(self.asset_dir)

    def create_asset_file(self, filename):
        filepath = op.join(self.asset_dir, filename)
        with open(filepath, 'w') as f:
            f.write(SCSS_CONTENT)
        return filepath

    def create_static_file(self, filename):
        filepath = op.join(self.static_dir, filename)
        with open(filepath, 'w') as f:
            f.write('nothing')
        return filepath

    def test_that_required_flask_app_attributes_exist(self):
        flask_app = Flask('__main__')
        for attr in ['static_folder', 'root_path', 'logger', 'before_request']:
            assert hasattr(flask_app, attr)

    def test_set_asset_dir_assets_scss(self):
        asset_scss_dir = op.join(self.test_data, 'assets', 'scss')
        os.makedirs(asset_scss_dir)
        scss = flaskext.flask_scss.Scss(self.app)
        self.assertEqual(scss.asset_dir, asset_scss_dir)

    def test_set_asset_dir_assets(self):
        asset_dir = op.join(self.test_data, 'assets')
        os.makedirs(asset_dir)
        scss = flaskext.flask_scss.Scss(self.app)
        self.assertEqual(scss.asset_dir, asset_dir)

    def test_set_asset_dir_none(self):
        scss = flaskext.flask_scss.Scss(self.app)
        self.assertIsNone(scss.asset_dir)

    def test_set_asset_dir_user_input(self):
        asset_scss_dir = op.join(self.test_data, 'assets2', 'scss')
        os.makedirs(asset_scss_dir)
        scss = flaskext.flask_scss.Scss(self.app,
                                        asset_dir=op.join(self.test_data,
                                                          'assets2'))
        self.assertEqual(scss.asset_dir, asset_scss_dir)

    def test_set_static_dir_static_css(self):
        static_css_dir = op.join(self.test_data, 'static', 'css')
        os.makedirs(static_css_dir)
        scss = flaskext.flask_scss.Scss(self.app)
        self.assertEqual(scss.static_dir, static_css_dir)

    def test_set_static_dir_static(self):
        static_dir = op.join(self.test_data, 'static')
        os.makedirs(static_dir)
        scss = flaskext.flask_scss.Scss(self.app)
        self.assertEqual(scss.static_dir, static_dir)

    def test_set_static_dir_none(self):
        scss = flaskext.flask_scss.Scss(self.app)
        self.assertIsNone(scss.static_dir)

    def test_set_static_dir_user_input(self):
        static_css_dir = op.join(self.test_data, 'static2', 'css')
        os.makedirs(static_css_dir)
        scss = flaskext.flask_scss.Scss(self.app,
                                        static_dir=op.join(self.test_data,
                                                          'static2'))
        self.assertEqual(scss.static_dir, static_css_dir)

    def test_set_hooks_no_static_dir(self):
        asset_dir = op.join(self.test_data, 'assets')
        os.makedirs(asset_dir)
        flaskext.flask_scss.Scss(self.app)
        self.assertFalse(self.app.before_request.called)

    def test_set_hooks_no_asset_dir(self):
        static_dir = op.join(self.test_data, 'static')
        os.makedirs(static_dir)
        flaskext.flask_scss.Scss(self.app)
        self.assertFalse(self.app.before_request.called)

    def test_set_hooks_ok(self):
        self.set_layout()
        scss = flaskext.flask_scss.Scss(self.app)
        self.assertTrue(self.app.before_request.called)
        self.assertEquals(self.app.before_request.call_count, 1)
        self.app.before_request.assert_called_with(scss.update_scss)

    def test_discover_scss(self):
        self.set_layout()
        self.create_asset_file('foo.scss')
        self.create_asset_file('foo.txt')
        scss = flaskext.flask_scss.Scss(self.app)
        scss.discover_scss()
        self.assertIn('foo.scss', scss.assets)
        self.assertNotIn('foo.txt', scss.assets)

    def test_update_scss_asset_to_update(self):
        self.set_layout()
        css_path = self.create_static_file('foo.css')
        scss_path = self.create_asset_file('foo.scss')
        os.utime(css_path, (time.time() - 10, time.time() - 10))
        os.utime(scss_path, (time.time() - 5, time.time() - 5))
        scss = flaskext.flask_scss.Scss(self.app)
        # check that the css file is older than the scss file
        self.assertGreater(op.getmtime(scss_path), op.getmtime(css_path))
        scss.update_scss()
        #verifies that css file has been modified
        self.assertGreater(op.getmtime(css_path), op.getmtime(scss_path))
        # verifies that the content of the css file has changed
        css_content = open(css_path).read()
        self.assertNotEquals(css_content, "nothing")

    def test_update_scss_nothing_to_update(self):
        self.set_layout()
        css_path = self.create_static_file('foo.css')
        scss_path = self.create_asset_file('foo.scss')
        os.utime(scss_path, (time.time() - 10, time.time() - 10))
        os.utime(css_path, (time.time() - 5, time.time() - 5))
        scss = flaskext.flask_scss.Scss(self.app)
        # check that the css file is newer than the scss file
        self.assertGreater(op.getmtime(css_path), op.getmtime(scss_path))
        scss.update_scss()
        #verifies that css file has been modified
        self.assertGreater(op.getmtime(css_path), op.getmtime(scss_path))
        # verifies that the content of the css file has NOT changed
        css_content = open(css_path).read()
        self.assertEquals(css_content, "nothing")

    def test_update_scss_update_only_changed_scss_files(self):
        self.set_layout()
        css_must_be_compiled_path = self.create_static_file('foo.css')
        css_must_not_change_path = self.create_static_file('bar.css')
        scss_newer_path = self.create_asset_file('foo.scss')
        scss_older_path = self.create_asset_file('bar.scss')

        os.utime(scss_older_path,
                 (time.time() - 10, time.time() - 10))
        os.utime(css_must_not_change_path,
                 (time.time() - 5, time.time() - 5))
        os.utime(scss_newer_path,
                 (time.time() - 5, time.time() - 5))
        os.utime(css_must_be_compiled_path,
                 (time.time() - 10, time.time() - 10))

        scss = flaskext.flask_scss.Scss(self.app)

        self.assertGreater(op.getmtime(css_must_not_change_path),
                           op.getmtime(scss_older_path))
        self.assertGreater(op.getmtime(scss_newer_path),
                           op.getmtime(css_must_be_compiled_path))
        scss.update_scss()

        self.assertGreater(op.getmtime(css_must_not_change_path),
                           op.getmtime(scss_older_path))
        self.assertGreater(op.getmtime(css_must_be_compiled_path),
                           op.getmtime(scss_newer_path))

        css_older_content = open(css_must_not_change_path).read()
        self.assertEquals(css_older_content, "nothing")

        css_newer_content = open(css_must_be_compiled_path).read()
        self.assertNotEquals(css_newer_content, "nothing")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
