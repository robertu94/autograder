.PHONY: test
%:%.py
	PYTHONPATH=..:$$PYTHONPATH python3 -m unittest $^ -v
test:
	@PYTHONPATH=..:$$PYTHONPATH python3 -m unittest discover  -v
