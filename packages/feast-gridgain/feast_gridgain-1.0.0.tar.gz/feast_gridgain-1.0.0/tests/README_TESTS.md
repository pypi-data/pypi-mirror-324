# Ignite-Feast: Running Tests

This README provides detailed instructions on how to set up and run both unit tests and integration tests for the Ignite-Feast project.

## Prerequisites

Before running the tests, ensure you have the following installed:

1. Python 3.11.7
2. pip (Python package installer)
3. Apache Ignite (for integration tests)
4. GridGain (for GridGain-specific integration tests)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/gridgain-poc/ignite_feast.git
   cd ignite-feast
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package and its dependencies:
   ```
   pip install -e '.[test,coverage]'
   ```

4. Install test dependencies:
   ```
   pip install pytest pytest-asyncio pytest-cov
   ```

## Running Unit Tests

To run all unit tests:

```
pytest tests/unit
```

To run unit tests for a specific module:

```
pytest tests/unit/test_ignite_online_store.py
pytest tests/unit/gridgain_online_store_tests.py
```

## Running Integration Tests

Before running integration tests, ensure that you have Apache Ignite and/or GridGain running and properly configured.
Before running the integration tests for gridgain, please add the credentials and url for the gridgain instance in test_gridgain_online_store.py

To run all integration tests:

```
pytest tests/integration -m integration
```

To run integration tests for a specific module:

```
pytest tests/integration/test_gridgain_online_store.py -m integration
pytest tests/integration/test_ignite_integration.py -m integration
```

Note: The `-m integration` flag is used to run only tests marked with the `integration` marker.

## Running Tests with Coverage

To run all tests (unit and integration) with coverage report:

```
pytest --cov=src/ignite_feast tests/
```

## Test Configuration

The `pyproject.toml` file includes the following test configuration:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
asyncio_mode = "strict"
markers = [
    "integration: marks tests as integration tests (deselect with '-m \"not integration\"')",
]

[tool.pytest.asyncio]
default_fixture_loop_scope = "function"
```

This configuration:
- Sets the test directory to `tests`
- Identifies test files starting with `test_`
- Sets the asyncio mode to "strict"
- Defines an "integration" marker for integration tests

## Writing New Tests

When writing new tests:

1. Create test files in the appropriate directory:
   - Unit tests go in `tests/unit/`
   - Integration tests go in `tests/integration/`
2. Name test files with the prefix `test_`.
3. Use the `pytest` framework for writing tests.
4. For asynchronous tests, use the `pytest-asyncio` plugin.
5. Mark integration tests with the `@pytest.mark.integration` decorator.

Example of an integration test:

```python
import pytest
from feast_gridgain.online_store import IgniteOnlineStore

@pytest.mark.integration
def test_some_integration_functionality():
    store = IgniteOnlineStore()
    # Add your integration test logic here
    assert some_condition

@pytest.mark.integration
@pytest.mark.asyncio
async def test_async_integration_functionality():
    # Add your async integration test logic here
    assert await some_async_condition
```

## Continuous Integration

If you're using a CI/CD pipeline, you can run all tests using:

```
pytest tests/
```

For running only unit tests in CI:

```
pytest tests/unit/
```

For running only integration tests in CI:

```
pytest tests/integration/ -m integration
```

## Troubleshooting

1. If you encounter import errors, ensure that your `PYTHONPATH` includes the project root directory.
2. Make sure all dependencies are correctly installed in your virtual environment.
3. For integration tests, veri