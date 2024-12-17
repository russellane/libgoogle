include Python.mk
PROJECT	= libgoogle
COV_FAIL_UNDER = 100
lint :: mypy
doc :: README.md
README.md:
	./mkdoc $(PROJECT) >$@
