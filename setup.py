from distutils.core import setup

setup(
  name='traverse_json',
  packages=['traverse_json'],
  version='0.1',
  description='Parse JSON object as if it were a file system',
  author='Feiyang Niu',
  author_email='statech.forums@gmail.com',
  url='https://github.com/statech/traverse_json',
  download_url='https://github.com/statech/traverse_json/archive/0.1.tar.gz',
  keywords=['json', 'traverse', 'path'],
  classifiers=[],
  install_requires=[
    'requests'
  ]
)
