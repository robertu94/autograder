"""
Install the autograder
"""
import os
import subprocess
import sys
from setuptools import setup

def readme():
    """make the readme the long description"""
    with open("README.md") as infile:
        return infile.read()

def clean_up_share():
    """Execute make clean to clean up the examples"""
    for directory in ['share/examples/docker_example', 'share/examples/example']:
        subprocess.call(['make', 'clean'], cwd=directory)

def share_files():
    """return the list of files to package"""
    clean_up_share()
    share_prefix = os.path.join(sys.prefix, "share/autograder")
    file_list = []
    for root, dirs, files in os.walk('share'):
        new_root = root.partition('share/')[2]
        current_dir_list = []
        if '.hg' in dirs:
            dirs.remove('.hg')
        if '.autograder' in dirs:
            dirs.remove('.hg')
        for data_file in files:
            current_dir_list.append(os.path.join(root, data_file))
        file_list.append((os.path.join(share_prefix, new_root), current_dir_list))
    return file_list


setup(name="autograder",
      author="Robert Underwood",
      author_email="rr.underwood94@gmail.com",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Education",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Topic :: Software Development :: Testing",
      ],
      data_files=share_files(),
      description="A automatic testing and grading framework in python",
      entry_points={
          'console_scripts': ['autograder=autograder.controller.autograder:main']
      },
      extras_require={
          'docs': ['sphinx', 'sphinx_rtd_theme'],
      },
      install_requires=[
          'PyYAML'
      ],
      keywords="autograder education docker",
      license="bsd",
      long_description=readme(),
      packages=[
          'autograder',
          'autograder.controller',
          'autograder.report',
          'autograder.test',
          'autograder.source',
          'autograder.discover'
          ],
      url="https://www.cs.clemson.edu/acm",
      version="1.0.0",
      zip_safe=False
     )

