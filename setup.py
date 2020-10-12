from __future__ import absolute_import, print_function

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from os import path
from shutil import move


def readme(filename: str = 'README.md') -> str:
    """
    read the contents of your README.md file
    :return: contents of README.md
    """

    this_directory = path.abspath(path.dirname(__file__))

    with open(path.join(this_directory, filename), encoding='utf-8') as file:
        return file.read()


class CustomExtension(Extension):
    def __init__(self, name, sources, base_dir, *args, **kw):
        super().__init__(name, sources, *args, **kw)
        self.base_dir = base_dir


class CustomBuild(build_ext):
    def build_extension(self, ext: CustomExtension):
        if isinstance(ext, CustomExtension):
            ext.sources = [path.join(ext.base_dir, each) for each in ext.sources]

        super().build_extension(ext)

        if isinstance(ext, CustomExtension):
            raw_output = self.get_ext_fullpath(ext.name)

            filename = path.basename(raw_output)
            pathname = path.dirname(raw_output)

            output = path.join(pathname, ext.base_dir, filename)

            move(raw_output, output)


custom_extension = CustomExtension(name='_core',
                                   sources=['flow-network.cpp', 'py-api.cpp'],
                                   base_dir='flow_network/core',
                                   extra_compile_args=['-std=c++14', '-W', '-fPIC'])

setup(
    name='flow-network',
    version='0.0.3',
    author='Lucien Shui',
    author_email='lucien@lucien.ink',
    url='https://github.com/LucienShui/flow-network',
    description='Flow Network C++ Implementation',
    packages=find_packages(),
    ext_modules=[custom_extension],
    cmdclass={'build_ext': CustomBuild},
    long_description=readme(),
    long_description_content_type='text/markdown'
)
