import setuptools

from appbbt import __version__


def read_content(filename):
    return open(filename, 'r', encoding='utf-8').read()


setuptools.setup(
    name='appbbt',
    description=read_content('README.md'),
    version=__version__,
    packages=['appbbt'],
    zip_safe=False,
    install_requires=[
        'Appium-Python-Client',
        'zope.cachedescriptors',
    ]
)
