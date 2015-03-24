from setuptools import setup, find_packages
setup(
      name = "VISapi",
      version = "0.1.0",
      packages = find_packages(),
      install_requires = ['SQLAlchemy', 'VISlib', 'werkzeug', 'webob', 'visapps >= 2.2']
)
