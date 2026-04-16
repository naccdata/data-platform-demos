.PHONY: lint format check test all

all: lint check

lint:
	uv run ruff check demo/

format:
	uv run ruff format demo/

check:
	uv run mypy demo/ --ignore-missing-imports

# Build Docker images
build-python-uploader:
	docker build -f demo/python-uploader/Dockerfile -t naccdata/python-uploader .

build-cli-uploader:
	docker build -f demo/fwcli/Dockerfile --platform linux/amd64 -t naccdata/cli-uploader .

build-r-uploader:
	docker build -f demo/r-uploader/Dockerfile -t naccdata/r-uploader .
