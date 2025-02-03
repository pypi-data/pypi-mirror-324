.DEFAULT_GOAL := help
CODE = casers tests benches
POETRY_RUN = poetry run
TEST = $(POETRY_RUN) pytest $(args)

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: format lint test  ## Run format lint test

.PHONY: install-poetry
install-poetry:  ## Install poetry
	pip install poetry==1.8.5

.PHONY: install
install:  ## Install dependencies
	poetry install -E pydantic

.PHONY: install-docs
install-docs:  ## Install docs dependencies
	poetry install --only docs

.PHONY: publish
publish:  ## Publish package
	@$(POETRY_RUN) maturin upload

.PHONY: build-rs
build-rs:  ## Build .so files
	$(POETRY_RUN) maturin develop

.PHONY: format-rs
format-rs:  ## Formatting Rust code
	cargo fmt

.PHONY: lint-rs
lint-rs:  ## Check Rust code
	cargo check

.PHONY: test
test:  ## Test with coverage
	$(TEST) --ignore=benches --cov=./

.PHONY: test-fast
test-fast:  ## Test until error
	$(TEST) --exitfirst

.PHONY: test-failed
test-failed:  ## Test failed
	$(TEST) --last-failed

.PHONY: lint
lint:  ## Check code
	$(POETRY_RUN) black --check $(CODE)
	$(POETRY_RUN) pytest --dead-fixtures --dup-fixtures
	$(POETRY_RUN) mypy $(CODE)

.PHONY: format
format:  ## Formatting code
	$(POETRY_RUN) black $(CODE)

.PHONY: bump
bump:  ## Bump version (commit and tag)
	$(POETRY_RUN) cz bump --major-version-zero

.PHONY: clean
clean:  ## Clean
	rm -rf site || true
	rm -rf dist || true
	rm -rf htmlcov || true

.PHONY: benchmark
benchmark:  ## Benchmark
	$(TEST) benches/test_to_camel.py

.PHONY: benchmark-all
benchmark-all:  ## Benchmark all
	$(TEST) benches
