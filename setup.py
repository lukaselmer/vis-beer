from setuptools import setup, find_packages
setup(
      name = "vis-beer",
      version = "0.0.1",
      packages = find_packages(),
      install_requires = ['SQLAlchemy', 'VISlib', 'werkzeug', 'webob', 'visapps >= 2.2']
)
