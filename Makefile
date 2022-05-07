# WARNING: `make` *requires* the use of tabs, not spaces, at the start of each command
.DEFAULT_GOAL := help

# declares .PHONY which will run the make command even if a file of the same name exists
.PHONY: help
help:			## Help command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Displays the recommended formatting changes.
lint:
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src odinuge/yapf:latest yapf \
	--style '{based_on_style: pep8, dedent_closing_brackets: true, coalesce_brackets: true}' \
	--no-local-style --verbose --recursive --diff --parallel directus tests examples

# Format code in place to conform to lint check
format:
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src odinuge/yapf:latest yapf \
	--style '{based_on_style: pep8, dedent_closing_brackets: true, coalesce_brackets: true}' \
	--no-local-style --verbose --recursive --in-place --parallel directus tests examples

## Pyflakes check for any unused variables/classes
pyflakes:
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src python:3.8 \
	/bin/bash -c "pip install --upgrade pyflakes && python -m pyflakes /src && echo 'pyflakes passed!'"

# Start local instance 
start:
	docker-compose up -d

quick-start:
	make start
	bash quick-start.sh localhost

destroy:
	docker-compose down -v

test:
	docker-compose -f docker-compose.test.yml up -d
	docker-compose -f docker-compose.test.yml exec pytest /bin/bash -c "apt-get update && apt-get install -y --no-install-recommends jq"
	docker-compose -f docker-compose.test.yml exec pytest /bin/bash -c "cd /directus-sdk && bash quick-start.sh directus && pip install -r requirements.txt"
	docker-compose -f docker-compose.test.yml exec pytest /bin/bash -c "cd /directus-sdk && BASE_URL=http://directus:8055 pytest -v"
	docker-compose -f docker-compose.test.yml down -v

deploy:
	python setup.py bdist_wheel
	pip install twine
	twine upload --username=${TWINE_USERNAME} --password=${TWINE_PASSWORD} --verbose dist/*

ci_deploy:
	pip install -r requirements.txt
	python setup.py bdist_wheel
	pip install twine
	twine upload --username=${TWINE_USERNAME} --password=${TWINE_PASSWORD} --verbose dist/*