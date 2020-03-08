publish:
	poetry build
	poetry publish -r hexlet

lint:
	poetry run flake8 page_loader

push:
	git add -A
	git commit -m "Auto Commit"
	git push
