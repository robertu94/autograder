.PHONY: clean tags develop install docs
install: 
	sudo python3 setup.py install
develop: docs
	sudo python3 setup.py develop
tags: $(wildcard **/*.py)
	ctags $(wildcard **/*.py)
docs:
	$(MAKE) -C docs html man
clean:
	find . -name "__pycache__" -exec rm -rf {} \+
	$(MAKE) -C docs clean
