Software Architecture Document
================================================================================

Logical
--------------------------------------------------------------------------------
The methods are roughly grouped by function in separate source files

- controller - main methods for program control
	- autograder - main command line method for the autograder
	- grade\_project - main grading routine
	- setup - parse configuration, and configure global state of the autograder
	- environment - build and prepare test cases
- discover - methods for determine what tests to run
    - users - methods for enumerating users to be graded
    - reporters - methods for enumerating reports to be generated
    - tests - methods for enumerating tests to be run
    - handin - methods for enumerating users from Clemson's Handin system
- source - methods for interacting with source code repositories
	- update - update user repositories
	- clone - clone new user repositories
	- clean - clean up used repositories
	- build - build user and autograder source code
- test - methods for running tests on user code
	- run - run tests and record the results
	- parse - parse the output of test results in well-known formats
	- grade - convert parsed results into a score
- report - methods for reporting test results
	- reports - generate reports that will be sent out
	- formatters - format reports that will be sent out
	- send - send reports to email or files

Process
--------------------------------------------------------------------------------

The program uses a process pool based architecture where each user is graded by a single process.
This could be overwritten by writing multi process test cases.
Multiprocessing can be disabled by using the setting `project.multiprocess=1` in the project configuration or on the command line.
By default, it will spawn one process for each core on the machine.


Deployment
--------------------------------------------------------------------------------

Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `python` version 3.3 or higher
- `python-yaml` 

build dependencies

- `make` drives the build of the project
- `python-setuptools` used to package the library

Optional dependencies

- `awk` - manage svn repositories
- `date` - used in unit test code
- `docker` - container based test environments
- `cgroup-lite` - container based test environments on Ubuntu
- `git` - manage git repositories
- `hg` - manage mercurial repositories
- `make` - used for make based source code builds.
- `svn` - manage svn repositories
- `xargs` - manage svn repositories
- `python-sphinx` - generate documentation
- `python-sphinx_rtd_theme` - theme used for web documentation

Create An Instance Of the Autograder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To deploy the auto grader:

1. Install dependencies listed above using your package manager
2. As an administrator run `make install`
3. As an administrator install a default configuration to `/etc/autograder.conf`.
   Sample configuration can be found the examples directory.
4. Run the autograder via `autograder config.json`
5. Optionally place in crontab or systemd timer

Data
--------------------------------------------------------------------------------
Data in the autograder are divided into a set of python dictionaries.
Elements marked as provisional may change in the near future.

- settings - a configuration for a run of the autograder
- users - a list of users
- results - the results for a single user

settings 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- project:
    - method - method of enumerating class. It can be one of {"discover","json","csv"}
    - file - if method is "csv" or "json" the list of list of student usernames
    - student - a pattern to match for a subset of student usernames to run; if unspecified, then all usernames run
    - name - name of the project
    - testdir - directory of files that should be copied into the build directory.  They will be copied into a '.autograder' directory at the root of the repository.
    - version - version of the settings module to use.  It should be an integer.  It will be incremented whenever a change is made to the json settings file interface
- prepare:
    - method - type of clean to use. It can be one of {"git","hg","noop","svn","script", "docker"}
    - command - when clean method is "script" the command to use to script
- update:
    - method - type of update to use. It can be one of {"git","hg","noop","svn","script"}
    - command - when update method is "script" the command to use to clean
    - forced - always run tests after an update
- build:
    - method - type of build method to use. It can be one of {"make","script","docker"}
    - command - when build method is "script" the command to use to build
    - timeout - how long to allow the build to run, 5 seconds if not specified.
    - dockerfile - path to the dockerfile to be used in docker builds
- tests[] - a list of one or more test objects that contain
    - run:
        - method - type of grading to preform. It can be one of {"script","docker"}
        - command - when run method is "script" the command to use to run this must output one of the passable formats
        - input - what input to pass to the script
        - timeout - how long to run the test, 5 seconds if not specified.
        - constraints - when run method "docker", a list of flags to pass to docker to limit resources
        - stderr - how to handle standard error, it can be separate, combined with stdout, or dropped
    - parse:
        - method - type of parsing to preform. It can be one of {"tap","script"}
        - input - when the parse method is script, what input format to use It can be one of {"json"}
        - output - when the parse method is script, what output format to use It can be one of {"json"}
        - command - when grade method is "script" the command to use to parse results
        - timeout - how long to run the test, 5 seconds if not specified.
    - score:
        - method - how to score the parsed results. It can be one of {"passfail","points","script"}
        - command - when score method is "script" the command to use to parse results must output two integers to stdout separated by a space indicating points earned and points possible
        - input - when the parse method is script, what input format to use It can be one of {"json"}
        - timeout - how long to run the test, 5 seconds if not specified.
        - min_points - the minimum number of points that will be assigned for this section
        - free_points - the number of points that are essentially extra
        - points_possible - maximum number of points possible for this test
- reports[] - a list of one or more reporting tasks
    - formatter_method - types of reporting to preform. It can be one of {}
    - send_method - types of sending methods. It can be one of {"email","file"}
    - source - where to send the report from output from for email
    - destination - where to place the report.  For json and csv this should be a path, for email this should be an email address.  This field can be expanded using the following format codes:
        - '%e' the students email address
        - '%u' the students username
        - '%d' the date
    - separate - true when that separate reports should be generated for each student
    - subject - the subject when sent via email.
    - command - when the reporting method is "script" the command use to report the output
    - detail - amount of detail to report. It is a list that can contain {"output","result","score"}
    - summarize - class include the summary [if not separate] or student summary[if separate]
- logging
    - logfile - where output should be logged to disk
    - file_verbosity - what level of output to show in the logfile
    - console_verbosity - what level of output to show to the console

results 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The results structure is laid out as follows:

.. code:: json

  {
    "user1": [
      {
        "output": {
          "stdout": "this is the stdout1\\n",
          "stderr": "this is the stderr1\\n",
          "return": 0,
          "time": 1.2,
          "error": false
        },
        "results": {
          "passed": 7,
          "failed": 1,
          "skipped": 0,
          "errors": 0,
          "total": 8
        },
        "points": {
          "earned": 7,
          "possible": 8
        }
      },
      {
        "output": {...},
        "results": {...},
        "points": {...}
      }
    ],
    "user2": [...]
  }


-   stdout - ASCII encoded string of the stdout of the process
-   stderr - ASCII encoded string of the stderr of the process
-   return - integer return code from the process
-   time - floating point value corresponding to the runtime
-   error - true if the process was killed or the test runner encountered an error. 
-   passed - integer number of test cases passed
-   failed - integer number of test cases failed
-   skipped - integer number of test cases skipped
-   errors - integer number of tests cases ending in an error
-   total - integer sum of the previous 4 values
-   earned - integers number of points earned
-   possible - integer number of points possible

users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The users structure is laid out as follows:

.. code:: json

  [
    {
      "directory": "example",
      "email": "example@foobar.com",
      "username": "example",
      "repo": "https://github.com/robertu94/autograder"
      "leader": "aslan"
    },
    {...},
    ...
  ]

-   directory - string corresponding to the path to the repo on disk
-   email - string corresponding to the users email address
-   username - string corresponding to the users username
-   repo - where the code should be cloned from
-   [provisional] leader - used when there are multiple users
    in a group for a single project, the user that actually runs
    the test.

Security
--------------------------------------------------------------------------------

Aside from extensive logging, there are currently very few security
countermeasures implemented.  See future improvements for a list of planned
security related features.

Known Issues
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- The source code based clean methods such as `clean.hg,` `clean.git`, and
  `clean.svn` do not detect files created in their source code directories:
  ".hg", ".git", and ".svn" respectively.  This could allow users to store
  state between runs of the autograder in the source code repository.  This can
  be mitigated by using the clean.script clean function instead.  The container
  based version should not be vulnerable to this attack.
- There are no resource limits applied to running user processes.  A
  maliciously crafted program could cause the program to crash via fork-bomb or
  other resource intensive attack.  The container based version will use
  c-groups to implement resource limits.  This will greatly reduce
  vulnerabilities to this type of attack.
- The executed programs are not currently executed on an isolated file system.
  This means that maliciously crafted programs could potentially edit or delete
  files that the user running the auto grader process has permission to modify,
  view, or execute including but not limited to files in the users home
  directory, copies of the source code owned by other users, or the grade
  result file.  Some of these attacks can be can be mitigated by running the
  auto grader with a separate user with limited privileges.  This can be further
  reduced by running the child processes as a different user using the
  run.script method with the su/sudo commands.  Finally, the container based
  version of the test runner should not be vulnerable to this method of attack
  because it will execute the children on a jailed file system.
- The executed programs are not isolated from the network.  This would allow
  programs to download or upload additional resources from the Internet.  This
  could allow users to upload the auto grader test cases or other protected
  code.  The container based version will use c-groups to isolate the container
  from the host network stack.  This will mitigate this form of attack.  If
  network accesses is required, the container's network could be forwarded
  through a proxy to block "illegal" access.
- Avoid placing source code repositories (git,svn,hg) above the user
  directories,  They could potentially be reset to an earlier state when
  performing a clean operation.  This issue is resolved by the container based
  version.


Development
--------------------------------------------------------------------------------

Run Unit Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Install dependencies
2. Change into the test directory
3. Execute make

Future work
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Future improvement shall be listed as issues on the GitHub repository.
