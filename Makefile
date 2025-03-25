VERSION=$(shell grep ^version pyproject.toml | gawk -F"[= ]" '{print $$NF}' | tr -d '"')
NAME=$(shell grep ^name pyproject.toml | gawk -F"[= ]" '{print $$NF}' | tr -d '"')
DIR:=${CURDIR}
EXAMPLE_DIR:=$(DIR)/extras/example_app_pkg
MAKE:=make
src_files:=$(shell find $(DIR) -type f -name '*.py')
PYTHON:=python3

.PHONY: all name version lint git_tag example-image test docs publish

all: lint test build

tag:
	git tag -a v$(VERSION) -m " auto-tagged"

version: pyproject.toml
	echo $(VERSION)

name: pyproject.toml
	echo $(NAME)

poetry.lock: pyproject.toml
	poetry lock

lint: poetry.lock deploydocus2  tests
	isort deploydocus2 tests #docs/source extras/simple_example_json_server/simplejsonserver/basichttp.py extras/example_app_pkg
	black deploydocus2 tests #docs/source extras/simple_example_json_server/simplejsonserver/basichttp.py extras/example_app_pkg
	flake8 deploydocus2 tests #docs/source extras/simple_example_json_server/simplejsonserver/basichttp.py extras/example_app_pkg
	$(DIR)/scripts/dmypy.sh deploydocus2 tests #extras/simple_example_json_server/simplejsonserver/basichttp.py extras/example_app_pkg

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
	PYTHONPATH=src:extras INTEGRATION=0 pytest tests

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