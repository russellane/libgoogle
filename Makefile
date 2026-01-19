include Python.mk
PROJECT	= libgoogle
COV_FAIL_UNDER = 100
lint :: mypy
doc :: mkdoc-readme

.PHONY: mkdoc-readme
mkdoc-readme:
	./mkdoc $(PROJECT) >README.md
