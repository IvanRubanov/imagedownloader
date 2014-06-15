from setuptools import setup

setup(name='imagedownloader',
      version='0.1',
      description='The image downloader from xhtml pages',
      url='http://github.com/IvanRubanov/imagedownloader',
      author='Ivan Rubanov',
      author_email='rubanovio@gmail.com',
      license='BSD',
      packages=['imagedownloader'],
      install_requires=[
          'beautifulsoup4',
      ],
      zip_safe=False)