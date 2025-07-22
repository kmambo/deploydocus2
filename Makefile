AWK:=/usr/local/bin/gawk
VERSION=$(shell grep ^version pyproject.toml | $(AWK) -F"[= ]" '{print $$NF}' | tr -d '"')
NAME=$(shell grep ^name pyproject.toml | $(AWK) -F"[= ]" '{print $$NF}' | tr -d '"')
DIR:=${CURDIR}
EXAMPLE_DIR:=$(DIR)/extras/example_app_pkg
MAKE:=make
src_files:=$(shell find $(DIR) -type f -name '*.py')
PYTHON:=python3.13
RUNNER_CMD:=poetry run

.PHONY: all name version lint git_tag example-image test docs publish

all: lint test build

version: pyproject.toml
	echo $(VERSION)

tag: version
	git tag -a v$(VERSION) -m "auto-tagged"

name: pyproject.toml
	echo $(NAME)

poetry.lock: pyproject.toml
	poetry lock

lint: poetry.lock deploydocus2 tests
	$(RUNNER_CMD) isort deploydocus2 tests
	$(RUNNER_CMD) black deploydocus2 tests
	$(RUNNER_CMD) flake8 deploydocus2 tests
	$(RUNNER_CMD) $(DIR)/scripts/dmypy.sh deploydocus2 tests

sync: poetry.lock
	poetry sync --no-root

build: sync
	poetry build

publish: sync
	poetry publish --build

render:
	helm template chart-instance k8s/defaultchart | yq -C | less -R

example-image: $(EXAMPLE_DIR)/Dockerfile $(EXAMPLE_DIR)/basichttp.py pyproject.toml
	docker build $(EXAMPLE_DIR) -t python-httpserver:$(VERSION)

kind-load: example-image
	kind load docker-image python-httpserver:$(VERSION) -n deploydocus

test: sync
	PYTHONPATH=src:extras INTEGRATION=0 $(RUNNER_CMD) pytest tests -v

cov:
	PYTHONPATH=src:extras INTEGRATION=0 $(RUNNER_CMD) pytest --cov=deploydocus2 \
		--cov-report annotate \
		--cov-report html \
		tests/

docs:
	$(MAKE) -C docs html

.PHONY: preview-docs
preview-docs: docs
	$(PYTHON) -m http.server 9000 --bind=127.0.0.1 --directory docs/build/html

.PHONY: site
site:
	$(MAKE) -C docs/project_site build

.PHONY: preview-site
preview-site: site
	$(MAKE) -C docs/project_site preview


.PHONY: deploy-site
deploy-site: site
	firebase deploy  --only hosting:deploydocus