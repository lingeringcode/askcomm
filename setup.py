from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'askcomm',
  packages = ['askcomm'],
  version = '0.0.2',
  description = 'A set of search patterns that query a corpus of event-based and community-detected tweets, but it could be modified to query most social-network (node-edge) data.',
  author = 'Chris A. Lindgren',
  author_email = 'chris.a.lindgren@gmail.com',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url = 'https://github.com/lingeringcode/askcomm/',
  download_url = 'https://github.com/lingeringcode/askcomm/',
  install_requires = ['pandas','tqdm'],
  keywords = ['corpus querying', 'search patterns', 'event-based corpus'],
  classifiers = [],
  include_package_data=True
)
