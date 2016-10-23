from distutils.core import setup

try:
    long_description = open('README.rst', 'rt').read()
except:
    long_description = ''


setup(
  name='constructible',
  py_modules=['constructible'],  # this must be the same as the name above
  version='0.4.1',
  description='Exact Constructible Numbers Representation',
  long_description=long_description,
  author='Leonhard Vogt',
  author_email='leonhard.vogt@gmx.ch',
  url='https://github.com/leovt/constructible',  # use the URL to the github repo
  download_url='https://github.com/leovt/constructible/tarball/0.4.1',
  keywords=[],  # arbitrary keywords
  classifiers=[],
)
