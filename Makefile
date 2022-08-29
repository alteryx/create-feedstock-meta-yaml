.PHONY: clean
clean:
	find . -name '*.pyo' -delete
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	find . -name '*~' -delete

.PHONY: installdeps
installdeps:
	python -m pip install -r requirements.txt
	pre-commit install

.PHONY: test
test:
	python create_feedstock_meta_yaml/test_create_feedstock_meta_yaml.py

.PHONY: lint
lint:
	isort --check-only create_feedstock_meta_yaml
	black create_feedstock_meta_yaml -t py310 --check

.PHONY: lint-fix
lint-fix:
	black create_feedstock_meta_yaml -t py310
	isort create_feedstock_meta_yaml
