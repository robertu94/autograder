Software Architecture Document
================================================================================

Logical
--------------------------------------------------------------------------------
The methods are roughly grouped by function in separate source files

- controller
	- autograder - main command line method for the autograder
	- grade\_project - main grading routine
	- setup - parse configuration, and configure global state of the autograder
	- environment - build and prepare test cases
	- project - enumeration methods
- source
	- update - update student repositories
	- clone - clone new student repositories
	- clean - clean up used repositories
	- build - build student and autograder source code
- test - methods for running tests
	- run - run tests and record the results
	- parse - parse the output of test results in well-known formats
	- grade - convert parsed results into a score
- report - methods for reporting test results
	- reports - generate reports that will be sent out
	- formatters - format reports that will be sent out
	- send - send reports to email or files

Process
--------------------------------------------------------------------------------
The process is designed to be single threaded, and single process.  Student
results are processed in serial fashion.

Deployment
--------------------------------------------------------------------------------

### Dependancies

Dependencies
- python3

build dependencies
- make

optional dependencies
- date - used in unit test code
- docker - container based test environments
- git - manage git repositories
- hg - manage mercurial repositories
- make - used for make based source code builds.
- svn - manage svn repositories
- xargs manage svn repositories
- awk manage svn repositories

### Create an instance of the Autograder
To deploy the auto grader:

1. Install dependencies
2. As an administrator run `make install`
3. Run the autograder via `autograder config.json`
4. Optionally place in crontab or systemd timer

Data
--------------------------------------------------------------------------------
Data in the autograder are divided into a set of python dictionaries

- settings - A dictionary where all configuration is stored. The layout is described in
  `controllers/setup.py`
- results -	A list of dictionaries containing where all output, parsing results,
  and grades pertaining to a student are stored before being passed to the
  report functions.  Its format is specified in `grade_project.py`
- students - A list of dictionaries containing information specific to each
  student.  Its format is described in `grade_project.py`

Security
--------------------------------------------------------------------------------
Aside from extensive logging, there are currently very few security
countermeasures implemented.  See future improvements for a list of planned
security related features.

### Known issues

- The source code based clean methods such as `clean.hg,` `clean.git`, and
  `clean.svn` do not detect files created in their source code directories:
  ".hg", ".git", and ".svn" respectively.  This could allow students to store
  state between runs of the autograder in the source code repository.  This can
  be mitigated by using the clean.script clean function instead.  The container
  based version should not be vulnerable to this attack.
- There are no resource limits applied to running student processes.  A
  maliciously crafted program could cause the program to crash via fork-bomb or
  other resource intensive attack.  The container based version will use
  c-groups to implement resource limits.  This will greatly reduce
  vulnerabilities to this type of attack.
- The executed programs are not currently executed on an isolated file system.
  This means that maliciously crafted programs could potentially edit or delete
  files that the user running the auto grader process has permission to modify,
  view, or execute including but not limited to files in the users home
  directory, copies of the source code owned by other students, or the grade
  result file.  Some of these attacks can be can be mitigated by running the
  auto grader with a separate user with limited privileges.  This can be further
  reduced by running the child processes as a different user using the
  run.script method with the su/sudo commands.  Finally, the container based
  version of the test runner should not be vulnerable to this method of attack
  because it will execute the children on a jailed file system.
- The executed programs are not isolated from the network.  This would allow
  programs to download or upload additional resources from the Internet.  This
  could allow students to upload the auto grader test cases or other protected
  code.  The container based version will use c-groups to isolate the container
  from the host network stack.  This will mitigate this form of attack.  If
  network accesses is required, the container's network could be forwarded
  through a proxy to block "illegal" access.
- Avoid placing source code repositories (git,svn,hg) above the student
  directories,  They could potentially be reset to an earlier state when
  performing a clean operation.  This issue is resolved by the container based
  version.


Development
--------------------------------------------------------------------------------

### Run Unit Tests

1. Install dependencies
2. Change into the test directory
3. Execute make

### Future work

1.	Containerized test environments for running student code
2.  C library for interfacing with MSP based micro controllers
3.	Additional well known formats for the parser such as JUnit, python unittest
4.  Full suite of unittest to verify functionality
5.  Systemd service file + timer parameterized on config file name

