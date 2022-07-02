install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install dist/hexlet_code-0.1.0-py3-none-any.whl

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

make lint:
	poetry run flake8 page_loader