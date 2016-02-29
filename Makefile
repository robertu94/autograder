.PHONY: clean
tags: $(wildcard **/*.py)
	ctags $(wildcard **/*.py)
clean:
	find . -name "__pycache__" -exec rm -rf {} \+

