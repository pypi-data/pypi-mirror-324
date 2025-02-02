from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='dj_obj',
  version='1.0.1',
  author='SODT',
  author_email='svsharygin@icloud.com',
  description='',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/lum0vi/new_library',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'https://github.com/lum0vi/new_library'
  },
  python_requires='>=3.9'
)
