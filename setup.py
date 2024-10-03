from setuptools import setup, find_packages

setup(
  name='PrivateSign',
  version='0.3.0',
  packages=find_packages(),
  include_package_data=True,
  description='A secure sign PDF files SDK',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  author='Brian',
  author_email='brian.hoag@paperlogic.co.jp',
  url='https://github.com/brianhoag1/PrivateSign',
  classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
  ],
  python_requires='>=3.6',
  install_requires=[
      'requests',
  ],
)