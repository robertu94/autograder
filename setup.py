from setuptools import setup

def readme():
    with open("README.md") as infile:
        return infile.read()

setup(name="autograder",
      author="Robert Underwood",
      author_email="rr.underwood94@gmail.com",
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Intended Audience :: Education",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Topic :: Software Development :: Testing",
      ],
      description="A automatic testing and grading framework in python",
      entry_points={
          'autograder': ['autograder=autograder.controller.autograder:main']
      },
      keywords="autograder education docker",
      license="bsd",
      long_description=readme(),
      packages=['autograder'],
      url="https://www.cs.clemson.edu/acm",
      version="0.0.1",
      zip_safe=False
     )

