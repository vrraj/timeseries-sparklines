# Timeseries SVG Makefile

.PHONY: install dev api run example test build clean format

# Install package in development mode
install:
	pip install -e .

# Install with development dependencies
dev:
	pip install -e ".[dev]"

# Install with API dependencies
api:
	pip install -e ".[api]"

# Run the API server
run:
	python run_api.py

# Run example script
example:
	python example.py

# Run tests
test:
	python -m pytest tests/ -v

# Run tests with coverage
test-cov:
	python -m pytest tests/ --cov=timeseries_svg --cov-report=html

# Build package
build:
	python -m build

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Format code
format:
	black src/timeseries_svg/
	ruff check src/timeseries_svg/ --fix

# Type check
type-check:
	mypy src/timeseries_svg/
