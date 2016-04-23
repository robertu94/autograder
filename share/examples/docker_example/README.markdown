# Example of Traditional Autograder

This is a full example project with five students

Here are the expected results:

-   Student 1 - Perfect score
-   Student 2 - Missing makefile
-   Student 3 - Missing source file
-   Student 4 - No output
-   Student 5 - Wrong output
-   Student 6 - Floating point error
-   Student 7 - Extremely long output

## Run this example

-   Install the autograder and its dependencies
-   Ensure that you can run Docker's "hello world" application and an OS
	container of your choice.
-   Copy the file `defaults.json` to `/etc/autograder.conf`
-   Create the file `~/.hgrc` if it doesn't exist and set at least username like so:

```ini
[ui]
username = Firstname Lastname <youremail@example.com>
```

-   Run the `prepare.sh` scripts in `project` and `repository`
-   Issue the command `autograder config.json` to run the autograder
