from setuptools import setup, find_packages

setup(name='nghsync',
      version='0.0.1',
      description='',
      url='https://github.com/lokijuhy/notion-gh-sync',
      packages=find_packages(),
      python_requires='>3.7.0',
      install_requires=[
            'ghapi',
            'notion-client',
      ],
      entry_points={
            'console_scripts': ['nghsync=nghsync.nghsync:main'],
      },
      zip_safe=False)
