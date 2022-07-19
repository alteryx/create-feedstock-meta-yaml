.PHONY: clean
clean:
	find . -name '*.pyo' -delete
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	find . -name '*~' -delete

.PHONY: installdeps
installdeps:
	python -m pip install -r requirements.txt

.PHONY: test
test:
	python create_feedstock_meta_yaml/test_create_feedstock_meta_yaml.py
