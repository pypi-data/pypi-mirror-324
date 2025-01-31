# -*- coding: utf-8 -*-
#
# Copyright © 2015,2016 Mathieu Duponchelle <mathieu.duponchelle@opencreed.com>
# Copyright © 2015,2016 Collabora Ltd
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

"""
A syntax highlighting module
"""
import os

from hotdoc.core.formatter import Formatter
from hotdoc.core.extension import Extension

from hotdoc.utils.utils import recursive_overwrite
from hotdoc.utils.loggable import warn, Logger
from hotdoc.core.exceptions import ConfigError

DESCRIPTION = """
This extension uses prism to syntax highlight code
snippets.
"""


HERE = os.path.dirname(__file__)


Logger.register_warning_code('syntax-invalid-theme', ConfigError,
                             'syntax-extension')


class SyntaxHighlightingExtension(Extension):
    """
    The actual syntax highlighting implementation
    """
    extension_name = 'syntax-highlighting-extension'
    argument_prefix = 'syntax-highlighting'
    needs_licensing = False

    def __init__(self, app, project):
        Extension.__init__(self, app, project)
        self.__asset_folders = set()
        self.activated = False
        self.keep_markup = False

    def __formatting_page_cb(self, formatter, page):
        prism_theme = Formatter.theme_meta.get('prism-theme', 'prism-tomorrow')
        prism_theme_path = '%s.css' % os.path.join(
            HERE, 'prism', 'themes', prism_theme)

        if os.path.exists(prism_theme_path):
            page.output_attrs['html']['dark-stylesheets'].add(prism_theme_path)
        else:
            warn('syntax-invalid-theme', 'Prism has no theme named %s' %
                 prism_theme)

        prism_light_theme = Formatter.theme_meta.get(
            'prism-light-theme', 'prism')
        prism_light_theme_path = '%s.css' % os.path.join(
            HERE, 'prism', 'themes', prism_light_theme)

        if os.path.exists(prism_light_theme_path):
            page.output_attrs['html']['light-stylesheets'].add(
                prism_light_theme_path)
        else:
            warn('syntax-invalid-theme', 'Prism has no theme named %s' %
                 prism_light_theme)

        page.output_attrs['html']['scripts'].add(
            os.path.join(HERE, 'prism', 'components', 'prism-core.js'))
        page.output_attrs['html']['scripts'].add(
            os.path.join(HERE, 'prism', 'plugins', 'autoloader',
                         'prism-autoloader.js'))
        page.output_attrs['html']['scripts'].add(
            os.path.join(HERE, 'prism_autoloader_path_override.js'))
        if self.keep_markup:
            page.output_attrs['html']['scripts'].add(
                os.path.join(HERE, 'prism', 'plugins', 'keep-markup',
                             'prism-keep-markup.js'))

        folder = os.path.join('html', 'assets', 'prism_components')
        self.__asset_folders.add(folder)

    def __formatted_cb(self, project):
        ipath = os.path.join(HERE, 'prism', 'components')
        for folder in self.__asset_folders:
            opath = os.path.join(self.app.output, folder)
            recursive_overwrite(ipath, opath)

    @classmethod
    def get_assets_licensing(cls):
        if SyntaxHighlightingExtension.needs_licensing:
            return {
                'prism': {
                    'url': 'https://prismjs.com/',
                    'license': 'MIT'
                }
            }
        return {}

    def setup(self):
        super(SyntaxHighlightingExtension, self).setup()
        if not self.activated:
            return

        SyntaxHighlightingExtension.needs_licensing = True

        for ext in self.project.extensions.values():
            ext.formatter.formatting_page_signal.connect(
                self.__formatting_page_cb)
        self.project.formatted_signal.connect(self.__formatted_cb)

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group('Syntax highlighting extension',
                                          DESCRIPTION)
        group.add_argument('--disable-syntax-highlighting',
                           action="store_true",
                           help="Deactivate the syntax highlighting extension",
                           dest='disable_syntax_highlighting')
        group.add_argument('--keep-markup-in-code-blocks',
                           action='store_true',
                           help='Keep HTML markup in custom <code> blocks.' +
                                'This allows inserting hyperlinks, etc.',
                           dest='keep_markup_in_code_blocks')

    def parse_config(self, config):
        super(SyntaxHighlightingExtension, self).parse_config(config)
        self.activated = \
            not bool(config.get('disable_syntax_highlighting', False))
        self.keep_markup = \
            bool(config.get('keep_markup_in_code_blocks', False))
