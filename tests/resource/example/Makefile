all: clean test
test:
	autograder config.json
clean:
	$(RM) *.txt autograder.log prof-output.json
	$(RM) -r student{1..7}
