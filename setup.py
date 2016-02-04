#
# Copyright (c) 2007-2013. The YARA Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import re
import os
import platform
import subprocess
import sys

from setuptools import setup, Command, Extension
from setuptools.command.build_ext import build_ext


args = sys.argv[1:]
macros = []

if '--with-profiling' in args:
    macros.append(('PROFILING_ENABLED', '1'))
    args.remove('--with-profiling')


def get_sources(source):
    result = []
    exclusions = set("cuckoo.c magic.c".split())
    for directory, _, files in os.walk(source):
        for x in files:
            if x.endswith(".c") and x not in exclusions:
                result.append(os.path.join(directory, x))

    return result

sources = ["rekall_yara/yara-python/yara-python.c"]
sources += get_sources("rekall_yara/yara/libyara/")

def parse_version():
    version = open("version.txt").read()
    m = re.search(r"\d+\.\d+\.\d+", version)
    if m:
        return m.group(0)
    return version


class BuildExtCommand(build_ext):
    """Custom handler for the build_ext command."""

    project_builder = None

    def run(self):
        # Except on Linux we need to run the configure script.
        if platform.system() != "Windows":
            subprocess.check_call(
                ["./configure", "--without-crypto",
                 "--disable-magic", "--disable-cuckoo",
                 "--disable-dmalloc"],
                cwd="rekall_yara/yara/")

        build_ext.run(self)


class CleanCommand(Command):
    description = ("custom clean command that forcefully removes "
                   "dist/build directories")
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        if os.getcwd() != self.cwd:
            raise RuntimeError('Must be in package root: %s' % self.cwd)

        os.system('rm -rf ./build ./dist')


setup(script_args=args,
      name='rekall_yara',
      long_description=open("README.txt").read(),
      cmdclass=dict(
          build_ext=BuildExtCommand,
          clean=CleanCommand,
      ),
      version='3.4.0',
      packages=["rekall_yara"],
      package_data={
          "rekall_yara": ["config.h"],
      },
      author='Victor M. Alvarez',
      author_email='plusvic@gmail.com;vmalvarez@virustotal.com',
      zip_safe=False,
      ext_modules=[Extension(
          name='rekall_yara/yara',
          sources=sources,
          libraries=['ssl', 'crypto'],
          include_dirs=[
              'rekall_yara/yara/yara-python',
              'rekall_yara/yara/libyara/include',
              'rekall_yara/yara/libyara/',
              'rekall_yara/yara/',
              '.',
          ],
          define_macros=macros,
          extra_compile_args=['-std=gnu99']
      )])
