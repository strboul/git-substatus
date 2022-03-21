define check_pip_module
	$(if $(shell pip show $(1)),,$(error "module '$(1)' not found."))
endef


define echo_section
	@printf "\33[33m\n%s\n%s\n\33[0m" $(1) "==========================="
endef


define ask_prompt
	@printf "%s\nAre you sure? [y/N]" $(1) && read ans && [ $${ans:-N} = y ]
endef


VERSION := $(shell ./get_version.sh __version__)
PY_VERSION := $(shell ./get_version.sh __py_version__)


all: typecheck black test install docker-build clean


install:
	$(call echo_section,"installing")
	pip install .


test: unittest clean


unittest:
	$(call echo_section,"running tests")
	python -m unittest --verbose


typecheck:
	$(call check_pip_module,"mypy")
	$(call echo_section,"static type checking")
	mypy --pretty --show-error-context --show-error-codes git_substatus


coverage:
	$(call check_pip_module,"coverage")
	$(call echo_section,"measuring code coverage")
	coverage run --source git_substatus -m unittest && coverage report


black:
	$(call check_pip_module,"black")
	$(call echo_section,"checking code formatting with black")
	python -m black --check .


black-apply:
	$(call check_pip_module,"black")
	$(call echo_section,"applying code formatting with black")
	python -m black .


clean:
	$(call echo_section,"cleaning")
	find . -depth -name __pycache__ -exec rm -rf {} \; && \
	find . -depth -name *.pyc -exec rm -rf {} \; && \
	find . -depth -name *.mypy_cache -exec rm -rf {} \; && \
	find . -depth -name .coverage -exec rm {} \; && \
	rm -rf tests/generated-test-proj-dir


tag-create:
	$(call ask_prompt,"creating tag \"v$(VERSION)\".")
	git tag "v$(VERSION)"


tag-push:
	$(call ask_prompt,"pushing tag \"$(VERSION)\" to master.")
	git push origin "v$(VERSION)"


docker-build:
	$(call echo_section,"building the docker image")
	docker build -t strboul/git-substatus:"$(VERSION)" --build-arg PY_VERSION="$(PY_VERSION)" .
	docker tag strboul/git-substatus:"$(VERSION)" strboul/git-substatus:latest
