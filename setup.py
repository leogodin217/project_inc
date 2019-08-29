from setuptools import setup

setup(name='supplyon_uploader',
      version='1.0',
      description='Uploads job data to the SupplyOn Portal',
      author='Leo Godin',
      author_email='leogodin217@gmail.com',
      packages=['supplyon_uploader'],
      install_requires=['pandas', 'zeep', 'pyodbc'],
      zip_safe=False)