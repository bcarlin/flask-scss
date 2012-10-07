from __future__ import with_statement
try:
    import unittest2 as unittest
except ImportError:
    import unittest # NOQA
import os
import os.path as op
import shutil
from mock import Mock, patch
from flask import Flask
from flaskext import scss
import time

SCSS_CONTENT = "a { color: red; text-decoration: none; }"


class ScssTest(unittest.TestCase):

    def setUp(self):
        self.test_data = op.join(os.getcwd(), 'test_data')
        os.makedirs(self.test_data)
        self.app = Mock()
        self.app.root_path = self.test_data
        self.app.config = {'SCSS_LOAD_PATHS': []}
        self.app.static_folder = op.join(self.test_data, 'static')

    def tearDown(self):
        shutil.rmtree(self.test_data, ignore_errors=True)

    def set_layout(self, base=None):
        base = base or self.test_data
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
        for attr in ['static_folder', 'root_path', 'logger', 'before_request',
                     'testing', 'debug']:
            assert hasattr(flask_app, attr)

    def test_set_asset_dir_assets_scss(self):
        asset_scss_dir = op.join(self.test_data, 'assets', 'scss')
        os.makedirs(asset_scss_dir)
        scss_inst = scss.Scss(self.app)
        self.assertEqual(scss_inst.asset_dir, asset_scss_dir)

    def test_set_asset_dir_assets(self):
        asset_dir = op.join(self.test_data, 'assets')
        os.makedirs(asset_dir)
        scss_inst = scss.Scss(self.app)
        self.assertEqual(scss_inst.asset_dir, asset_dir)

    def test_set_asset_dir_none(self):
        scss_inst = scss.Scss(self.app)
        self.assertIsNone(scss_inst.asset_dir)

    def test_set_asset_dir_user_input(self):
        asset_scss_dir = op.join(self.test_data, 'assets2', 'scss')
        os.makedirs(asset_scss_dir)
        scss_inst = scss.Scss(self.app,
                              asset_dir=op.join(self.test_data, 'assets2'))
        self.assertEqual(scss_inst.asset_dir, asset_scss_dir)

    def test_set_asset_dir_from_app_conf(self):
        asset_scss_dir = op.join(self.test_data, 'assets', 'bar')
        self.app.config['SCSS_ASSET_DIR'] = asset_scss_dir
        os.makedirs(asset_scss_dir)
        scss_inst = scss.Scss(self.app)
        self.assertEqual(scss_inst.asset_dir, asset_scss_dir)

    def test_local_asset_dir_must_override_app_conf(self):
        asset_scss_dir = op.join(self.test_data, 'assets', 'bar')
        asset_scss_dir2 = op.join(self.test_data, 'assets2', 'bar')
        self.app.config['SCSS_ASSET_DIR'] = asset_scss_dir
        os.makedirs(asset_scss_dir)
        os.makedirs(asset_scss_dir2)
        scss_inst = scss.Scss(self.app, asset_dir=asset_scss_dir2)
        self.assertEqual(scss_inst.asset_dir, asset_scss_dir2)

    def test_set_static_dir_static_css(self):
        static_css_dir = op.join(self.test_data, 'static', 'css')
        os.makedirs(static_css_dir)
        scss_inst = scss.Scss(self.app)
        self.assertEqual(scss_inst.static_dir, static_css_dir)

    def test_set_static_dir_static(self):
        static_dir = op.join(self.test_data, 'static')
        os.makedirs(static_dir)
        scss_inst = scss.Scss(self.app)
        self.assertEqual(scss_inst.static_dir, static_dir)

    def test_set_static_dir_none(self):
        scss_inst = scss.Scss(self.app)
        self.assertIsNone(scss_inst.static_dir)

    def test_set_static_dir_user_input(self):
        static_css_dir = op.join(self.test_data, 'static2', 'css')
        os.makedirs(static_css_dir)
        scss_inst = scss.Scss(self.app,
                              static_dir=op.join(self.test_data, 'static2'))
        self.assertEqual(scss_inst.static_dir, static_css_dir)

    def test_set_static_dir_from_app_conf(self):
        static_scss_dir = op.join(self.test_data, 'static', 'bar')
        self.app.config['SCSS_STATIC_DIR'] = static_scss_dir
        os.makedirs(static_scss_dir)
        scss_inst = scss.Scss(self.app)
        self.assertEqual(scss_inst.static_dir, static_scss_dir)

    def test_local_static_dir_must_override_app_conf(self):
        static_scss_dir = op.join(self.test_data, 'static', 'bar')
        static_scss_dir2 = op.join(self.test_data, 'static2', 'bar')
        self.app.config['SCSS_STATIC_DIR'] = static_scss_dir
        os.makedirs(static_scss_dir)
        os.makedirs(static_scss_dir2)
        scss_inst = scss.Scss(self.app, static_dir=static_scss_dir2)
        self.assertEqual(scss_inst.static_dir, static_scss_dir2)

    def test_set_hooks_no_static_dir(self):
        asset_dir = op.join(self.test_data, 'assets')
        os.makedirs(asset_dir)
        scss.Scss(self.app)
        self.assertFalse(self.app.before_request.called)

    def test_set_hooks_no_asset_dir(self):
        static_dir = op.join(self.test_data, 'static')
        os.makedirs(static_dir)
        scss.Scss(self.app)
        self.assertFalse(self.app.before_request.called)

    def test_set_hooks_ok(self):
        self.set_layout()
        scss_inst = scss.Scss(self.app)
        self.assertTrue(self.app.before_request.called)
        self.assertEquals(self.app.before_request.call_count, 1)
        self.app.before_request.assert_called_with(scss_inst.update_scss)

    def test_discover_scss(self):
        self.set_layout()
        self.create_asset_file('foo.scss')
        self.create_asset_file('foo.txt')
        scss_inst = scss.Scss(self.app)
        scss_inst.discover_scss()
        self.assertIn(op.join(self.asset_dir, 'foo.scss'), scss_inst.assets)
        self.assertNotIn(op.join(self.asset_dir, 'foo.txt'), scss_inst.assets)

    def test_scss_discovery_is_recursive(self):
        self.set_layout()
        self.create_asset_file('foo.scss')
        asset_scss_dir = op.join(self.test_data, 'assets', 'bar')
        os.makedirs(asset_scss_dir)
        self.create_asset_file('bar/baz.scss')
        scss_inst = scss.Scss(self.app)
        scss_inst.discover_scss()
        self.assertIn(op.join(self.test_data, 'assets', 'bar', 'baz.scss'),
                      scss_inst.assets)

    def test_partial_scss_are_not_considered_assets(self):
        self.set_layout()
        self.create_asset_file('_bar.scss')
        scss_inst = scss.Scss(self.app)
        scss_inst.discover_scss()
        self.assertNotIn(op.join(self.asset_dir, '_bar.scss'), scss_inst.assets)

    def test_partial_scss_are_considered_partials(self):
        self.set_layout()
        self.create_asset_file('_bar.scss')
        scss_inst = scss.Scss(self.app)
        scss_inst.discover_scss()
        self.assertIn(op.join(self.asset_dir, '_bar.scss'), scss_inst.partials)

    def test_asset_tree_is_kept_in_static_dir(self):
        self.set_layout()
        asset_scss_dir = op.join(self.test_data, 'assets', 'bar')
        os.makedirs(asset_scss_dir)
        self.create_asset_file('bar/baz.scss')
        scss_inst = scss.Scss(self.app)
        scss_inst.discover_scss()
        asset = op.join(self.test_data, 'assets', 'bar', 'baz.scss')
        expected_dest = op.join(self.test_data, 'static', 'bar', 'baz.css')
        self.assertEqual(expected_dest, scss_inst.assets[asset],
                         "css folder not kept")

    def test_update_scss_asset_to_update(self):
        self.set_layout()
        css_path = self.create_static_file('foo.css')
        scss_path = self.create_asset_file('foo.scss')
        os.utime(css_path, (time.time() - 10, time.time() - 10))
        os.utime(scss_path, (time.time() - 5, time.time() - 5))
        scss_inst = scss.Scss(self.app)
        # check that the css file is older than the scss file
        self.assertGreater(op.getmtime(scss_path), op.getmtime(css_path))
        scss_inst.update_scss()
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
        scss_inst = scss.Scss(self.app)
        # check that the css file is newer than the scss file
        self.assertGreater(op.getmtime(css_path), op.getmtime(scss_path))
        scss_inst.update_scss()
        #verifies that css file has been modified
        self.assertGreater(op.getmtime(css_path), op.getmtime(scss_path))
        # verifies that the content of the css file has NOT changed
        css_content = open(css_path).read()
        self.assertEquals(css_content, "nothing")

    # might not be pertinent
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

        scss_inst = scss.Scss(self.app)

        self.assertGreater(op.getmtime(css_must_not_change_path),
                           op.getmtime(scss_older_path))
        self.assertGreater(op.getmtime(scss_newer_path),
                           op.getmtime(css_must_be_compiled_path))
        scss_inst.update_scss()

        self.assertGreater(op.getmtime(css_must_not_change_path),
                           op.getmtime(scss_older_path))
        self.assertGreater(op.getmtime(css_must_be_compiled_path),
                           op.getmtime(scss_newer_path))

        css_older_content = open(css_must_not_change_path).read()
        self.assertEquals(css_older_content, "nothing")

        css_newer_content = open(css_must_be_compiled_path).read()
        self.assertNotEquals(css_newer_content, "nothing")

    def test_css_is_refreshed_if_partials_are_updated(self):
        self.set_layout()
        css_must_be_compiled_path = self.create_static_file('foo.css')
        scss_path = self.create_asset_file('foo.scss')
        scss_partial_path = self.create_asset_file('_bar.scss')

        scss_inst = scss.Scss(self.app)

        os.utime(scss_partial_path,
                 (time.time() - 25, time.time() - 25))

        scss_inst.discover_scss()

        os.utime(scss_partial_path,
                 (time.time() - 5, time.time() - 5))
        os.utime(scss_path,
                 (time.time() - 15, time.time() - 15))
        os.utime(css_must_be_compiled_path,
                 (time.time() - 10, time.time() - 10))

        self.assertGreater(op.getmtime(css_must_be_compiled_path),
                           op.getmtime(scss_path))

        self.assertGreater(op.getmtime(scss_partial_path),
                           op.getmtime(css_must_be_compiled_path))

        scss_inst.update_scss()

        self.assertGreater(op.getmtime(css_must_be_compiled_path),
                           op.getmtime(scss_path))

        self.assertGreater(op.getmtime(css_must_be_compiled_path),
                           op.getmtime(scss_partial_path), "not refreshed")

        css_newer_content = open(css_must_be_compiled_path).read()
        self.assertNotEquals(css_newer_content, "nothing")

    def test_it_sets_up_refresh_hooks_if_application_is_in_test_mode(self):
        self.app.testing = True
        self.app.debug = False
        with patch.object(scss.Scss, 'set_hooks') as mock_set_hooks:
            scss.Scss(self.app)
            self.assertTrue(mock_set_hooks.called)

    def test_it_sets_up_refresh_hooks_if_application_is_in_debug_mode(self):
        self.app.testing = False
        self.app.debug = True
        with patch.object(scss.Scss, 'set_hooks') as mock_set_hooks:
            scss.Scss(self.app)
            self.assertTrue(mock_set_hooks.called)

    def test_it_sets_up_refresh_hooks_if_application_is_in_debug_and_testing_mode(self):
        self.app.testing = True
        self.app.debug = True
        with patch.object(scss.Scss, 'set_hooks') as mock_set_hooks:
            scss.Scss(self.app)
            self.assertTrue(mock_set_hooks.called)

    def test_it_does_not_set_up_refresh_hooks_if_application_is_not_in_debug_or_testing_mode(self):
        self.app.testing = False
        self.app.debug = False
        with patch.object(scss.Scss, 'set_hooks') as mock_set_hooks:
            scss.Scss(self.app)
            self.assertFalse(mock_set_hooks.called)

    def test_it_looks_for_an_app_load_path_settings(self):
        self.app.config['SCSS_LOAD_PATHS'].append('foo')
        scss.Scss(self.app)
        self.assertIn('foo', scss.pyScss.LOAD_PATHS)

    def test_it_looks_for_an_app_load_path_settings_with_multiple_paths(self):
        self.app.config['SCSS_LOAD_PATHS'].append('foo')
        self.app.config['SCSS_LOAD_PATHS'].append('bar')
        scss.Scss(self.app)
        self.assertIn('foo', scss.pyScss.LOAD_PATHS)
        self.assertIn('bar', scss.pyScss.LOAD_PATHS)

    def test_app_config_is_overridden_by_local_conf(self):
        self.app.config['SCSS_LOAD_PATHS'].append('foo')
        scss.Scss(self.app, load_paths=['bar'])
        self.assertIn('bar', scss.pyScss.LOAD_PATHS)

    def test_app_config_is_overridden_by_local_conf_with_multiple_paths(self):
        self.app.config['SCSS_LOAD_PATHS'].append('foo')
        scss.Scss(self.app, load_paths=['bar', 'baz'])
        self.assertIn('bar', scss.pyScss.LOAD_PATHS)
        self.assertIn('baz', scss.pyScss.LOAD_PATHS)

    def test_the_asset_dir_is_in_the_load_path(self):
        inst = scss.Scss(self.app, load_paths=['bar', 'baz'])
        self.assertIn(inst.asset_dir, scss.pyScss.LOAD_PATHS)

    def test_compile_scss_creates_subfolders_if_necessary(self):
        self.set_layout()
        asset_scss_dir = op.join(self.test_data, 'assets', 'bar')
        os.makedirs(asset_scss_dir)
        self.create_asset_file('bar/baz.scss')
        self.create_asset_file('foo.scss')
        op.join(self.test_data, 'assets', 'bar', 'baz.scss')
        expected_dest = op.join(self.test_data, 'static', 'bar', 'baz.css')

        scss_inst = scss.Scss(self.app)
        scss_inst.update_scss()
        self.assertTrue(os.path.exists(expected_dest))
        self.assertTrue(os.path.exists(os.path.join(self.test_data, 'static',
                                                    'foo.css')))

    def test_import_scheme_wrong_legacy(self):
        try:
            from flaskext.flask_scss import Scss
        except ImportError:
            assert False, "'from flaskext.flask_scss import Scss' should work"

    def test_import_scheme_legacy_ok(self):
        try:
            from flaskext.scss import Scss
        except ImportError:
            assert False, "'from flaskext.scss import Scss' should work"

    def test_import_scheme_new(self):
        try:
            from flask.ext.scss import Scss
        except ImportError:
            assert False, "'from flask.ext.scss import Scss' should work"


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
