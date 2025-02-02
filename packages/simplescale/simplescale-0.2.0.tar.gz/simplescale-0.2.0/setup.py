"""Setup module.
"""

import os
import setuptools
import sys

version = os.environ.get('PYPI_VERSION', '')
if not version:
  print('Environment variable PYPI_VERSION is not set')
  sys.exit(1)


setuptools.setup(
  name='simplescale',
  version=version,
  author='Nikhil Kothari',
  description='A simple gradio application to upscale images.',
  license='Apache',
  keywords='ai genai imaging upscaling esrgan gradio',
  url='https://github.com/nikhilk/itools/imscale',
  packages=[
    'simplescale'
  ],
  install_requires = [
    'gradio>=5.14.0'
  ],
  classifiers=[
    # From https://pypi.org/classifiers/
    'Development Status :: 3 - Alpha',
    'Environment :: GPU :: NVIDIA CUDA',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Artistic Software'
  ],
)
