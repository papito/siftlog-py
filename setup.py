from setuptools import setup

setup(name='siftlog',
      version='0.11',
      description='Structured JSON logging',
      long_description=(read('README.rst')
      url='http://github.com/papito/siftlog-py',
      author='Andrei Taranchenko',
      author_email='andrei360-git@yahoo.com',
      license='MIT',
      packages=['siftlog'],
      zip_safe=False,
      setup_requires=['nose>=1.0']
)
