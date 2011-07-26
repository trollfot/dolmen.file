from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.file'
version = '2.0a1'
readme = open(join('README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'ZODB3',
    'cromlech.file',
    'grokcore.component',
    'setuptools',
    'zope.component',
    'zope.contenttype',
    'zope.interface',
    'zope.schema',
    'zope.size',
    ]

tests_require = [
    ]

setup(name=name,
      version=version,
      description="A file representation package for Dolmen/Cromlech.",
      long_description=readme + '\n\n' + history,
      keywords='Cromlech Grok file',
      author='The Dolmen Team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      test_suite="dolmen.file",
      classifiers=[
          'Environment :: Web Environment',
          'Programming Language :: Python',
          ],
    )
