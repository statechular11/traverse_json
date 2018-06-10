import os
from distutils.core import setup

long_description = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.rst'
    )
).read()

if __name__ == "__main__":
    setup(
        name='traverse_json',
        packages=['traverse_json'],
        version='0.1',
        description='Parse JSON object as if it were a file system',
        author='Feiyang Niu',
        author_email='statech.forums@gmail.com',
        url='https://github.com/statech/traverse_json',
        keywords=['json', 'traverse', 'path'],
        install_requires=['requests'],
        license='MIT',
        long_description=long_description,
        scripts=[],
        data_files=[],
        classifiers=[]
    )
