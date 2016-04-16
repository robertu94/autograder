.PHONY: clean tags develop install
tags: $(wildcard **/*.py)
	ctags $(wildcard **/*.py)
clean:
	find . -name "__pycache__" -exec rm -rf {} \+
develop:
	sudo python3 setup.py develop
install:
	sudo python3 setup.py install

