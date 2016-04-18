.PHONY: clean tags develop install
install:
	sudo python3 setup.py install
develop:
	sudo python3 setup.py develop
tags: $(wildcard **/*.py)
	ctags $(wildcard **/*.py)
clean:
	find . -name "__pycache__" -exec rm -rf {} \+
