# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

#include .env
#export $(shell sed 's/=.*//' .env)

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# ========== Poetry stuff ========== #
shell: ## Activate Poetry shell
	poetry shell

install_poetry: ## Install Poetry
	curl -sSL https://install.python-poetry.org | python3 -

version: ## Check Poetry version
	poetry --version

config: ## Poetry config token
	poetry config pypi-token.pypi $$PYPI

publish: ## Poetry build and publish
	poetry publish --build

# ========== Build ========== #

build: ## Build package
	poetry build

test: ## Run tests
	pytest

# ========== Utils ========== #

clear: ## Clear repository
	rm -rf "${current_dir}/output"
	mkdir "${current_dir}/output"

try: clear ## Fill subject directory
	python "${current_dir}/example.py" \
		-bg="${current_dir}/example/small_bg.jpg" \
		-si="${current_dir}/example/wings.png" \
		-l1="${current_dir}/example/shikimori-glyph.png" \
		-l2="${current_dir}/example/shikimori-logo.png" \
		-he="${current_dir}/example/Noto_Serif/NotoSerif-Bold.ttf" \
		-t="${current_dir}/example/Noto_Serif/NotoSerif-Regular.ttf" \
		-s="${current_dir}/example/Noto_Serif_JP/NotoSerifJP-Bold.otf" \
		-out="${current_dir}/output/result.jpg"
