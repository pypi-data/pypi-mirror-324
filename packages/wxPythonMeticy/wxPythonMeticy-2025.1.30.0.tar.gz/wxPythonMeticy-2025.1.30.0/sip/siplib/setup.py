# SPDX-License-Identifier: BSD-2-Clause

# Copyright (c) 2024 Phil Thompson <phil@riverbankcomputing.com>


import glob

from setuptools import Extension, setup


# Build the extension module.
module_src = sorted(glob.glob('*.c'))

module = Extension('wx.siplib', module_src)

# Do the setup.
setup(
        name='wx_siplib',
        version='12.16.1',
        license='SIP',
        python_requires='>=3.9',
        ext_modules=[module]
     )
