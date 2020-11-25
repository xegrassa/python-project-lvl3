install:
	poetry install

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest --cov=tests

push:
	git add -A
	git commit -m "Auto Commit"
	git push
build:
	poetry build
package-install:
	pip install --user dist/*.whl
