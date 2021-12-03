.PHONY: install test typecheck coverage docker clean release


define check_pip_module
	$(if $(shell pip show $(1)),,$(error "module '$(1)' not found."))
endef


define echo_section
	@printf "\33[33m\n%s\n%s\n\33[0m" $(1) "=============================="
endef


VERSION := $(shell sed -n "s/__version__ = *\"\([^ ]*\)\"/\1/p" git_substatus/__init__.py)


all: typecheck black test install clean


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
	python -m black --check git_substatus


clean:
	$(call echo_section,"cleaning")
	find . -depth -name __pycache__ -exec rm -rf {} \; && \
	find . -depth -name *.pyc -exec rm -rf {} \; && \
	find . -depth -name *.mypy_cache -exec rm -rf {} \; && \
	find . -depth -name .coverage -exec rm {} \;


# release with twine: https://twine.readthedocs.io/en/latest/#using-twine
release-pypi:
	$(call echo_section,"releasing to PyPi")
	$(call check_pip_module,"twine")
	$(call check_pip_module,"wheel")
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload dist/*
	$(RM) -r build/ dist/ *.egg-info/


docker-build:
	$(call echo_section,"building the docker image")
	docker build -t strboul/git-substatus:$(VERSION) .
	docker tag strboul/git-substatus:$(VERSION) strboul/git-substatus:latest


docker-release:
	$(call echo_section,"releasing to https://hub.docker.com")
	@echo "Login with the Docker ID to push the image to Docker Hub."
	docker login -u strboul
	docker push strboul/git-substatus:$(VERSION)
	docker push strboul/git-substatus:latest
