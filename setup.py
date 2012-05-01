#!/usr/bin/env python

import os

from distutils.command.build_py     import build_py     as _build_py
from distutils.command.install      import install      as _install
from distutils.core import setup

class build_py(_build_py):
    """Specialised Python builder for Plex Plug-Ins and Scanners."""

    def get_module_outfile (self, build_dir, package, module):
        # Fix the bundle name
        if 'bundle' in package:
            # TODO: Remove hardcoding
            package = ['Plug-ins', 'EyeTV Info.bundle', 'Contents', 'Code']
        # Fix the scanner names
        if '' in package:
            package = [ 'Scanners', module[-6:] ]
        value = _build_py.get_module_outfile(self, build_dir, package, module)
        print build_dir, package, module, "=>", value
        return value

class install(_install):
    """Specialised installer for Plex Plug-Ins and Scanners."""

    def initialize_options (self):
        _install.initialize_options(self)
        self.warn_dir = 0

    sub_commands = [ ('install_lib',     _install.has_lib),
                     ('install_data',    _install.has_data)
                   ]

setup(name='Plex EyeTV Tools',
      version='0.1',
      description='A Plex (Laika) Scanner and a Plex Agent Bundle',
      author='Pekka Nikander',
      author_email='pekka.nikander@iki.fi',
      url='http://github.com/pekkanikander/Plex-EyeTV-Tools',
      packages=['EyeTV Info.bundle.Contents.Code'],
      py_modules = ['EyeTV Movies', 'EyeTV Series'],
      data_files= [( 'Plug-ins/EyeTV Info.bundle/Contents/',
                     [ 'EyeTV Info/bundle/Contents/Info.plist' ])],
      cmdclass={ 'build_py'     : build_py, 
                 'install'      : install,  },
     )

