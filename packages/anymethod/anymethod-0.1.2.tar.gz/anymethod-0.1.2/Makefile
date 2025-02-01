SHELL=/bin/bash -euo pipefail


.PHONY: build
build: dist

dist: src/**/* pyproject.toml README.md uv.lock
	uv lock
	rm -rf $@
	cd $(@D) && uv build -o dist


.PHONY: docs
docs: \
	docs/badge/coverage.svg \
	docs/badge/tests.svg

docs/badge/coverage.svg: .tmp/coverage.xml
	uv run genbadge coverage --local -i $< -o $@

docs/badge/tests.svg: .tmp/junit.xml
	uv run genbadge tests --local -i $< -o $@
