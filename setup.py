import os
from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(name='siftlog',
      version='0.12',
      description='Structured JSON logging',
      long_description=(read('README.rst')),
      url='http://github.com/papito/siftlog-py',
      author='Andrei Taranchenko',
      author_email='andrei360-git@yahoo.com',
      license='MIT',
      packages=['siftlog'],
      zip_safe=False,
      setup_requires=['nose>=1.0']
)
