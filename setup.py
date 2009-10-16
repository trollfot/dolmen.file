from os.path import join
from setuptools import setup, find_packages

version = '0.1'

setup(name='dolmen.file',
      version=version,
      description="A Zope3 File representation package.",
      long_description= "%s\n\n%s" % (
          open(join('src', 'dolmen','file', 'README.txt')).read(),
          open(join('docs', 'HISTORY.txt')).read(),
          ),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'grokcore.view',
          'zope.schema',
          'zope.security',
          'zope.interface',
          'zope.component',
          'zope.publisher',
          'zope.traversing',
          'zope.contenttype',
          'zope.app.file',
          'dolmen.builtins',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
