.PHONY: clean install test typecheck coverage

define check_pip_module
	$(if $(shell pip show $(1)),,$(error "module '$(1)' not found."))
endef

define echo_section
	@printf "\33[33m\n%s\n%s\n\33[0m" $(1) "=============================="
endef

all: typecheck test install clean

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

clean:
	$(call echo_section,"cleaning")
	find . -depth -name __pycache__ -exec rm -rf {} \; && \
	find . -depth -name *.pyc -exec rm -rf {} \; && \
	find . -depth -name *.mypy_cache -exec rm -rf {} \; && \
	find . -depth -name .coverage -exec rm {} \;

# release with twine: https://twine.readthedocs.io/en/latest/#using-twine
release:
	$(call echo_section,"releasing to PyPi")
	$(call check_pip_module,"twine")
	$(call check_pip_module,"wheel")
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload dist/*
	$(RM) -r build/ dist/ git_substatus.egg-info/
