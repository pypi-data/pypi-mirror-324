# coding: UTF-8

from pathlib import Path

from setuptools import (
    find_packages,
    setup,
)


ROOT_MODULE_NAME = 'improve'

BASE_DIR = Path(__file__).absolute().parent
ROOT_MODULE_PATH = BASE_DIR / 'src' / ROOT_MODULE_NAME


def _get_long_description() -> str:
    with open(BASE_DIR / 'README.md', 'r') as readme:
        return readme.read()


setup(
    name='improve',
    version='0.0.0a1',
    description='Python utils',
    long_description=_get_long_description(),
    long_description_content_type="text/markdown",
    author='Wilbur Mayffair',
    package_dir={
        '': 'src',
    },
    packages=find_packages(
        'src',
    ),
    entry_points={
        'console_scripts': (
            'waituntil = {}.utils.waituntil:main'.format(
                ROOT_MODULE_NAME,
            ),
            'chmtime = {}.utils.chmtime:main'.format(
                ROOT_MODULE_NAME,
            ),
        ),
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
