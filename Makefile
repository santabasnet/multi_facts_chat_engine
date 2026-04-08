PYTHON=python
UV=uv

.PHONY: install start dev clean

install:
	$(UV) sync

start:
	env -u VIRTUAL_ENV $(UV) run $(PYTHON) main.py

dev:
	env -u VIRTUAL_ENV $(UV) run $(PYTHON) main.py

clean:
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -r {} +