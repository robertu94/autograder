Developer Specification for Script Based Extensions
================================================================================

This document summarizes what information

Build
--------------------------------------------------------------------------------

### Behavior

The script should execute a build

### Input

No input is expected

### Output

No output is expected

### Errors

If there is a problem the script should return non-zero.

Clean
--------------------------------------------------------------------------------

### Behavior

The script should remove temporary files and other necessary tasks to prepare
for a new run

### Input

No input is expected

### Output

No output is expected

### Errors

If there is a problem the script should return non-zero.

Update
--------------------------------------------------------------------------------

### Behavior

The script should update the source to the latest version to be tested

### Input

No input is expected

### Output

No output is expected

### Errors

If there is a problem the script should return non-zero.

Clone
--------------------------------------------------------------------------------

### Behavior

This script should clone new source code repositories if they do not exist

### Input

No input is expected

### Output

No output is expected

### Errors

If there is a problem the script should return non-zero.

Run
--------------------------------------------------------------------------------

### Behavior

This should run automated unit/integration tests against the source code.  This
is the only code that you may assume will have access to the same file system as
the running tests.

### Input

Arbitrary text

### Output

Arbitrary text

### Errors

This script should set a non-zero return code on exit

Parse
--------------------------------------------------------------------------------

### Behavior

This should parse the stdout of the run command in order to aid in scoring.

### Input

Arbitrary text

### Output

JSON formatted dictionary with the following keys should be outputted to stdout:

passed - integer representing the number of tests passed
failed - integer representing the number of tests failed
skipped - integer representing the number of tests skipped
error - integer representing the number of errors that occured
total - integer representing the sum of the previous 4 keys

### Errors

If there is a problem the script should return non-zero.


Grade
--------------------------------------------------------------------------------

### Behavior

This should determine the number of points to assign to a given set of tests

### Input

A JSON dictionary that contains the following structure:



### Output

A JSON dictionary that contains the following keys should be outputted to
stdout:

points\_earned - integer that represents the total number of points earned
points\_possible - integer that represents the total number of points possible


### Errors

If there is a problem the script should return non-zero.

