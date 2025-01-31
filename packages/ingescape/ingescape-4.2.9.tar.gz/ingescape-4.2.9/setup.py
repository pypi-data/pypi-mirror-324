# -*- coding: utf-8 -*-
#  =========================================================================
# setup.py - fichier de configuration du module Ingescape
#
# Copyright (c) the Contributors as noted in the AUTHORS file.
# This file is part of Ingescape, see https://github.com/zeromq/ingescape.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =========================================================================
#

import sys
from setuptools import setup
from setuptools.extension import Extension
import os
import platform

from_sources = os.environ.get('FROM_SOURCES', default=None)
__version__ = "4.2.9"

macos_lib_dirs = '/usr/local/lib/' #TODO: use lib path instead of hardcoding
linux_lib_dirs = '/usr/local/lib/'
windows_x64_lib_dirs = 'C:\\Program Files\\ingescape\\lib\\'
windows_x86_lib_dirs = 'C:\\Program Files (x86)\\ingescape\\lib\\'

macos_lib_dirs_from_artifacts = './dependencies/macos/'
linux_lib_dirs_from_artifacts = './dependencies/linux/'
windows_x64_lib_dirs_from_artifacts = './dependencies/windows/x64/'
windows_x86_lib_dirs_from_artifacts = './dependencies/windows/x86/'

extra_objects = []
librairies = []
librairies_dirs = []

compile_args = []
link_args = []

if platform.system() == "Linux":

  if from_sources:
    extra_objects.append(linux_lib_dirs_from_artifacts + 'libingescape.a')
    extra_objects.append(linux_lib_dirs_from_artifacts + 'libzyre.a')
    extra_objects.append(linux_lib_dirs_from_artifacts + 'libczmq.a')
    extra_objects.append(linux_lib_dirs_from_artifacts + 'libzmq.a')
    extra_objects.append(linux_lib_dirs_from_artifacts + 'libsodium.a')
  else:
    extra_objects.append(linux_lib_dirs + 'libingescape.a')
    extra_objects.append(linux_lib_dirs + 'libzyre.a')
    extra_objects.append(linux_lib_dirs + 'libczmq.a')
    extra_objects.append(linux_lib_dirs + 'libzmq.a')
    extra_objects.append(linux_lib_dirs + 'libsodium.a')
  compile_args = ["-I/usr/local/include/python3.8", "-I/usr/local/include/python3.8", "-Wno-unused-result", "-Wsign-compare", "-g", "-fwrapv", "-O3", "-Wall"]
  link_args = ["-L/usr/local/lib", "-lcrypt", "-lpthread", "-ldl",  "-lutil", "-lm", "-lstdc++"]
elif platform.system() == "Darwin":
  if from_sources:
    extra_objects.append(macos_lib_dirs_from_artifacts + 'libingescape.a')
    extra_objects.append(macos_lib_dirs_from_artifacts + 'libzyre.a')
    extra_objects.append(macos_lib_dirs_from_artifacts + 'libczmq.a')
    extra_objects.append(macos_lib_dirs_from_artifacts + 'libzmq.a')
    extra_objects.append(macos_lib_dirs_from_artifacts + 'libsodium.a')
  else:
    extra_objects.append(macos_lib_dirs + 'libingescape.a')
    extra_objects.append(macos_lib_dirs + 'libzyre.a')
    extra_objects.append(macos_lib_dirs + 'libczmq.a')
    extra_objects.append(macos_lib_dirs + 'libzmq.a')
    extra_objects.append(macos_lib_dirs + 'libsodium.a')
  compile_args = ["-I/usr/local/include", "-Wno-nullability-completeness", "-Wno-expansion-to-defined"]
elif platform.system() == "Windows":
  if platform.machine().endswith('64'):
    librairies = ["libzmq",'libingescape', 'libzyre', 'libczmq', 'libsodium', "ws2_32", "Iphlpapi", 'Rpcrt4']
    if from_sources:
      librairies_dirs.append(windows_x64_lib_dirs_from_artifacts)
      sys.path.extend(windows_x64_lib_dirs_from_artifacts)
    else:
      librairies_dirs.append(windows_x64_lib_dirs)
      sys.path.extend(windows_x64_lib_dirs)
    compile_args = ["-DINGESCAPE_STATIC"]

#Use an environment variable instead of "install-option" to add the compile arg. We are not able to use 'python wheels' with 'install-option'
if from_sources:
    compile_args.append("-DFROM_SOURCES")

setup(
    ext_modules = [
        Extension(
            name = "ingescape",
            sources = [
                "./src/admin.c",
                "./src/agent.c",
                "./src/channels.c",
                "./src/compat.c",
                "./src/core.c",
                "./src/ingescape_python.c",
                "./src/monitor.c",
                "./src/network.c",
                "./src/performance.c",
                "./src/util.c"
            ],
            include_dirs = ["./include", "./dependencies/include/"],
            libraries = librairies,
            library_dirs = librairies_dirs,
            extra_objects = extra_objects,
            extra_compile_args = compile_args,
            extra_link_args = link_args
        )
    ]
)
