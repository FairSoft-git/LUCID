# Test Templates

> **Project:** [Project Name]  
> **Version:** 1.0  
> **Last Updated:** 2025-11-27  
> **Status:** Active

---

## Purpose

This document provides copy-paste templates for writing tests following LUCID principles and pytest best practices. All tests follow the **Arrange-Act-Assert (AAA)** pattern.

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Unit Test Templates](#unit-test-templates)
3. [Integration Test Templates](#integration-test-templates)
4. [End-to-End Test Templates](#end-to-end-test-templates)
5. [Fixture Templates](#fixture-templates)
6. [Parametrized Test Templates](#parametrized-test-templates)
7. [Exception Test Templates](#exception-test-templates)
8. [Mock Test Templates](#mock-test-templates)
9. [Async Test Templates](#async-test-templates)
10. [Test Naming Conventions](#test-naming-conventions)

---

## Quick Reference

```
tests/
├── unit/                    # Fast, isolated tests
│   └── test_<module>.py
├── integration/             # Component interaction tests
│   └── test_<feature>_integration.py
├── e2e/                     # Full workflow tests
│   └── test_<workflow>_e2e.py
├── fixtures/                # Shared test data
│   └── sample_data.py
└── conftest.py              # Shared fixtures
```

**Test Naming Pattern:**
```
test_<function_name>_<scenario>_<expected_result>
```

---

## Unit Test Templates

### Basic Unit Test

```python
"""
Unit tests for <module_name>.

Tests the <ClassName/function_name> in isolation.
"""
import pytest

from features.<module> import <function_or_class>


class TestFunctionName:
    """Tests for function_name()."""

    def test_function_name_with_valid_input_returns_expected(self):
        """Verify function returns expected result for valid input."""
        # Arrange
        input_value = "test_input"
        expected = "expected_output"

        # Act
        result = function_name(input_value)

        # Assert
        assert result == expected

    def test_function_name_with_empty_input_returns_default(self):
        """Verify function handles empty input gracefully."""
        # Arrange
        input_value = ""
        expected = "default"

        # Act
        result = function_name(input_value)

        # Assert
        assert result == expected
```

### Class Unit Test

```python
"""
Unit tests for <ClassName>.

Tests the <ClassName> methods in isolation.
"""
import pytest

from features.<module> import ClassName


class TestClassName:
    """Tests for ClassName."""

    # ===== Fixtures =====

    @pytest.fixture
    def instance(self):
        """Create a fresh instance for each test."""
        return ClassName(param1="value1", param2="value2")

    # ===== Initialization Tests =====

    def test_init_with_valid_params_creates_instance(self):
        """Verify constructor creates valid instance."""
        # Arrange
        param1 = "value1"
        param2 = "value2"

        # Act
        instance = ClassName(param1=param1, param2=param2)

        # Assert
        assert instance.param1 == param1
        assert instance.param2 == param2

    def test_init_with_missing_required_param_raises_error(self):
        """Verify constructor enforces required parameters."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            ClassName(param1="value1")  # Missing param2

    # ===== Method Tests =====

    def test_method_name_with_valid_input_returns_expected(self, instance):
        """Verify method returns expected result."""
        # Arrange
        input_value = "test"
        expected = "processed_test"

        # Act
        result = instance.method_name(input_value)

        # Assert
        assert result == expected

    # ===== Property Tests =====

    def test_property_name_returns_computed_value(self, instance):
        """Verify property computes correct value."""
        # Arrange
        expected = "computed_value"

        # Act
        result = instance.property_name

        # Assert
        assert result == expected
```

### Pure Function Test

```python
"""
Unit tests for pure utility functions.

These functions have no side effects and always return
the same output for the same input.
"""
import pytest

from features.utils.helpers import calculate_total, format_currency


class TestCalculateTotal:
    """Tests for calculate_total() pure function."""

    def test_calculate_total_with_positive_values_returns_sum(self):
        """Verify sum of positive values."""
        # Arrange
        values = [10.0, 20.0, 30.0]
        expected = 60.0

        # Act
        result = calculate_total(values)

        # Assert
        assert result == expected

    def test_calculate_total_with_empty_list_returns_zero(self):
        """Verify empty list returns zero."""
        # Arrange
        values = []
        expected = 0.0

        # Act
        result = calculate_total(values)

        # Assert
        assert result == expected

    def test_calculate_total_is_pure_function(self):
        """Verify function doesn't mutate input."""
        # Arrange
        values = [1.0, 2.0, 3.0]
        original = values.copy()

        # Act
        _ = calculate_total(values)

        # Assert
        assert values == original  # Input unchanged
```

---

## Integration Test Templates

### Database Integration Test

```python
"""
Integration tests for database operations.

Tests actual database interactions (not mocked).
"""
import pytest
from pathlib import Path

from features.database import DatabaseManager


class TestDatabaseIntegration:
    """Integration tests for DatabaseManager with real database."""

    # ===== Fixtures =====

    @pytest.fixture
    def temp_db_path(self, tmp_path):
        """Create temporary database path."""
        return tmp_path / "test_database.json"

    @pytest.fixture
    def db_manager(self, temp_db_path):
        """Create DatabaseManager with temporary database."""
        manager = DatabaseManager(temp_db_path)
        yield manager
        # Cleanup happens automatically (tmp_path)

    @pytest.fixture
    def populated_db(self, db_manager):
        """Create database with sample data."""
        sample_data = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
        ]
        for item in sample_data:
            db_manager.insert(item)
        return db_manager

    # ===== Tests =====

    def test_insert_and_retrieve_item_persists_data(self, db_manager):
        """Verify inserted item can be retrieved."""
        # Arrange
        item = {"id": 1, "name": "Test Item"}

        # Act
        db_manager.insert(item)
        result = db_manager.get_by_id(1)

        # Assert
        assert result == item

    def test_query_with_filter_returns_matching_items(self, populated_db):
        """Verify query filters work correctly."""
        # Arrange
        expected_count = 1

        # Act
        results = populated_db.query(name="Item 1")

        # Assert
        assert len(results) == expected_count
        assert results[0]["name"] == "Item 1"
```

### API Integration Test

```python
"""
Integration tests for API endpoints.

Tests HTTP request/response cycles with real handlers.
"""
import pytest
import json

from features.api import create_app


class TestAPIIntegration:
    """Integration tests for REST API endpoints."""

    # ===== Fixtures =====

    @pytest.fixture
    def client(self):
        """Create test client for API."""
        app = create_app(testing=True)
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def auth_headers(self):
        """Create authentication headers."""
        return {"Authorization": "Bearer test_token"}

    # ===== GET Endpoint Tests =====

    def test_get_items_returns_list(self, client):
        """Verify GET /items returns item list."""
        # Arrange
        expected_status = 200

        # Act
        response = client.get("/api/items")

        # Assert
        assert response.status_code == expected_status
        assert isinstance(response.json, list)

    def test_get_item_by_id_returns_item(self, client):
        """Verify GET /items/<id> returns specific item."""
        # Arrange
        item_id = 1
        expected_status = 200

        # Act
        response = client.get(f"/api/items/{item_id}")

        # Assert
        assert response.status_code == expected_status
        assert response.json["id"] == item_id

    def test_get_nonexistent_item_returns_404(self, client):
        """Verify GET /items/<id> returns 404 for missing item."""
        # Arrange
        item_id = 99999
        expected_status = 404

        # Act
        response = client.get(f"/api/items/{item_id}")

        # Assert
        assert response.status_code == expected_status

    # ===== POST Endpoint Tests =====

    def test_post_item_creates_new_item(self, client, auth_headers):
        """Verify POST /items creates new item."""
        # Arrange
        new_item = {"name": "New Item", "value": 100}
        expected_status = 201

        # Act
        response = client.post(
            "/api/items",
            data=json.dumps(new_item),
            content_type="application/json",
            headers=auth_headers,
        )

        # Assert
        assert response.status_code == expected_status
        assert "id" in response.json
```

### Service Integration Test

```python
"""
Integration tests for service layer.

Tests service methods with real dependencies.
"""
import pytest

from features.services import OrderService
from features.repositories import OrderRepository
from features.external import PaymentGateway


class TestOrderServiceIntegration:
    """Integration tests for OrderService with real dependencies."""

    @pytest.fixture
    def order_service(self, temp_db_path):
        """Create OrderService with real repository."""
        repository = OrderRepository(temp_db_path)
        payment = PaymentGateway(sandbox=True)  # Use sandbox mode
        return OrderService(repository, payment)

    def test_create_order_stores_in_database(self, order_service):
        """Verify order creation persists to database."""
        # Arrange
        order_data = {
            "customer_id": 1,
            "items": [{"product_id": 1, "quantity": 2}],
        }

        # Act
        order = order_service.create_order(order_data)

        # Assert
        retrieved = order_service.get_order(order.id)
        assert retrieved is not None
        assert retrieved.customer_id == order_data["customer_id"]
```

---

## End-to-End Test Templates

### Full Workflow E2E Test

```python
"""
End-to-end tests for complete user workflows.

Tests entire system from input to output.
"""
import pytest
from pathlib import Path

from scripts.main import Application


class TestUserWorkflowE2E:
    """E2E tests for complete user workflows."""

    @pytest.fixture
    def app(self, tmp_path):
        """Create application with temporary directories."""
        config = {
            "data_dir": tmp_path / "data",
            "output_dir": tmp_path / "output",
        }
        return Application(config)

    @pytest.fixture
    def sample_input_file(self, tmp_path):
        """Create sample input file."""
        input_file = tmp_path / "input.csv"
        input_file.write_text("id,name,value\n1,Item1,100\n2,Item2,200\n")
        return input_file

    def test_complete_import_analyze_export_workflow(
        self, app, sample_input_file, tmp_path
    ):
        """Verify complete data processing workflow."""
        # Arrange
        output_file = tmp_path / "output" / "results.json"

        # Act - Complete workflow
        app.import_data(sample_input_file)
        app.analyze()
        app.export(output_file)

        # Assert
        assert output_file.exists()
        results = json.loads(output_file.read_text())
        assert len(results["items"]) == 2
        assert results["summary"]["total"] == 300

    def test_workflow_with_invalid_input_provides_error(
        self, app, tmp_path
    ):
        """Verify workflow handles errors gracefully."""
        # Arrange
        invalid_file = tmp_path / "invalid.csv"
        invalid_file.write_text("corrupted,data\n")

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            app.import_data(invalid_file)

        assert "Invalid format" in str(exc_info.value)
```

### CLI E2E Test

```python
"""
End-to-end tests for command-line interface.

Tests CLI commands with real arguments.
"""
import pytest
from click.testing import CliRunner

from scripts.cli import cli


class TestCLIE2E:
    """E2E tests for CLI commands."""

    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def temp_dir(self, runner):
        """Create isolated filesystem for CLI tests."""
        with runner.isolated_filesystem() as temp_dir:
            yield Path(temp_dir)

    def test_cli_process_command_creates_output(self, runner, temp_dir):
        """Verify CLI process command works end-to-end."""
        # Arrange
        input_file = temp_dir / "input.txt"
        input_file.write_text("test data")
        output_file = temp_dir / "output.txt"

        # Act
        result = runner.invoke(cli, [
            "process",
            "--input", str(input_file),
            "--output", str(output_file),
        ])

        # Assert
        assert result.exit_code == 0
        assert output_file.exists()
        assert "Success" in result.output
```

---

## Fixture Templates

### conftest.py (Shared Fixtures)

```python
"""
Shared pytest fixtures for all tests.

Location: tests/conftest.py
"""
import pytest
from pathlib import Path
import json
import tempfile


# ===== Path Fixtures =====

@pytest.fixture
def project_root():
    """Return project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def data_dir(project_root):
    """Return data directory path."""
    return project_root / "data"


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# ===== Data Fixtures =====

@pytest.fixture
def sample_json_data():
    """Return sample JSON data for testing."""
    return {
        "items": [
            {"id": 1, "name": "Item 1", "value": 100},
            {"id": 2, "name": "Item 2", "value": 200},
        ],
        "metadata": {
            "count": 2,
            "version": "1.0",
        },
    }


@pytest.fixture
def sample_json_file(temp_dir, sample_json_data):
    """Create temporary JSON file with sample data."""
    file_path = temp_dir / "sample.json"
    file_path.write_text(json.dumps(sample_json_data, indent=2))
    return file_path


# ===== Mock Fixtures =====

@pytest.fixture
def mock_http_response():
    """Create mock HTTP response."""
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self.json_data = json_data
            self.status_code = status_code
            self.text = json.dumps(json_data)

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception(f"HTTP {self.status_code}")

    return MockResponse


# ===== Configuration Fixtures =====

@pytest.fixture
def test_config():
    """Return test configuration."""
    return {
        "debug": True,
        "log_level": "DEBUG",
        "timeout": 5,
    }
```

### Fixture Factory Pattern

```python
"""
Fixture factories for creating test objects.
"""
import pytest
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool = True


@pytest.fixture
def user_factory():
    """Factory for creating User objects with defaults."""
    def _create_user(
        id: int = 1,
        name: str = "Test User",
        email: str = "test@example.com",
        active: bool = True,
    ) -> User:
        return User(id=id, name=name, email=email, active=active)

    return _create_user


# Usage in tests:
def test_with_custom_user(user_factory):
    user = user_factory(name="Custom Name", active=False)
    assert user.name == "Custom Name"
    assert user.active is False
```

---

## Parametrized Test Templates

### Basic Parametrization

```python
"""
Parametrized tests for testing multiple inputs.
"""
import pytest

from features.utils import validate_email


class TestValidateEmail:
    """Parametrized tests for email validation."""

    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("user.name@example.co.uk", True),
        ("user+tag@example.com", True),
        ("invalid", False),
        ("@example.com", False),
        ("user@", False),
        ("", False),
    ])
    def test_validate_email_returns_expected(self, email, expected):
        """Verify email validation for various inputs."""
        # Act
        result = validate_email(email)

        # Assert
        assert result == expected


class TestCalculateDiscount:
    """Parametrized tests for discount calculation."""

    @pytest.mark.parametrize("price,percentage,expected", [
        (100.0, 10, 90.0),
        (100.0, 25, 75.0),
        (100.0, 50, 50.0),
        (100.0, 0, 100.0),
        (100.0, 100, 0.0),
        (0.0, 50, 0.0),
    ], ids=[
        "10% discount",
        "25% discount",
        "50% discount",
        "no discount",
        "100% discount",
        "zero price",
    ])
    def test_calculate_discount_returns_expected(
        self, price, percentage, expected
    ):
        """Verify discount calculation for various scenarios."""
        # Act
        result = calculate_discount(price, percentage)

        # Assert
        assert result == expected
```

### Parametrized Fixtures

```python
"""
Parametrized fixtures for testing with multiple configurations.
"""
import pytest


@pytest.fixture(params=["json", "csv", "xml"])
def file_format(request):
    """Parametrized fixture for file formats."""
    return request.param


@pytest.fixture(params=[
    {"name": "small", "size": 10},
    {"name": "medium", "size": 100},
    {"name": "large", "size": 1000},
])
def dataset_config(request):
    """Parametrized fixture for dataset sizes."""
    return request.param


def test_export_supports_format(exporter, file_format):
    """Verify exporter supports all file formats."""
    # This test runs 3 times (once per format)
    result = exporter.export(data, format=file_format)
    assert result is not None
```

---

## Exception Test Templates

### Testing Expected Exceptions

```python
"""
Tests for exception handling.
"""
import pytest

from features.validators import validate_age, ValidationError


class TestValidateAge:
    """Tests for age validation exceptions."""

    def test_validate_age_negative_raises_value_error(self):
        """Verify negative age raises ValueError."""
        # Arrange
        age = -5

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            validate_age(age)

        assert "Age cannot be negative" in str(exc_info.value)

    def test_validate_age_too_high_raises_value_error(self):
        """Verify unrealistic age raises ValueError."""
        # Arrange
        age = 200

        # Act & Assert
        with pytest.raises(ValueError, match=r"Age must be less than \d+"):
            validate_age(age)

    def test_validate_age_non_integer_raises_type_error(self):
        """Verify non-integer raises TypeError."""
        # Arrange
        age = "twenty"

        # Act & Assert
        with pytest.raises(TypeError):
            validate_age(age)


class TestCustomExceptions:
    """Tests for custom exception types."""

    def test_operation_raises_custom_exception(self):
        """Verify custom exception with attributes."""
        # Arrange
        invalid_input = {"missing": "required_field"}

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            process_input(invalid_input)

        error = exc_info.value
        assert error.field == "required_field"
        assert error.code == "MISSING_FIELD"
```

### Testing Exception Chaining

```python
def test_exception_chaining_preserves_cause(self):
    """Verify exception chaining preserves original cause."""
    # Arrange
    invalid_data = None

    # Act & Assert
    with pytest.raises(ProcessingError) as exc_info:
        process_data(invalid_data)

    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, TypeError)
```

---

## Mock Test Templates

### Basic Mocking

```python
"""
Tests using mocks for external dependencies.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock

from features.services import NotificationService


class TestNotificationService:
    """Tests for NotificationService with mocked dependencies."""

    def test_send_email_calls_smtp_client(self):
        """Verify send_email uses SMTP client correctly."""
        # Arrange
        mock_smtp = Mock()
        service = NotificationService(smtp_client=mock_smtp)
        recipient = "user@example.com"
        message = "Hello!"

        # Act
        service.send_email(recipient, message)

        # Assert
        mock_smtp.send.assert_called_once_with(
            to=recipient,
            body=message,
        )

    def test_send_email_failure_raises_notification_error(self):
        """Verify SMTP failure is wrapped in NotificationError."""
        # Arrange
        mock_smtp = Mock()
        mock_smtp.send.side_effect = ConnectionError("SMTP down")
        service = NotificationService(smtp_client=mock_smtp)

        # Act & Assert
        with pytest.raises(NotificationError):
            service.send_email("user@example.com", "Hello!")
```

### Patching External Calls

```python
"""
Tests using patch for external API calls.
"""
import pytest
from unittest.mock import patch

from features.weather import get_weather


class TestGetWeather:
    """Tests for weather API integration."""

    @patch("features.weather.requests.get")
    def test_get_weather_returns_temperature(self, mock_get):
        """Verify weather API response parsing."""
        # Arrange
        mock_get.return_value.json.return_value = {
            "main": {"temp": 72.5},
            "weather": [{"description": "sunny"}],
        }
        mock_get.return_value.status_code = 200

        # Act
        result = get_weather("New York")

        # Assert
        assert result["temperature"] == 72.5
        assert result["description"] == "sunny"

    @patch("features.weather.requests.get")
    def test_get_weather_api_error_raises_exception(self, mock_get):
        """Verify API error handling."""
        # Arrange
        mock_get.return_value.status_code = 500
        mock_get.return_value.raise_for_status.side_effect = Exception("API Error")

        # Act & Assert
        with pytest.raises(WeatherAPIError):
            get_weather("New York")
```

### Context Manager Mocking

```python
@patch("builtins.open", create=True)
def test_read_config_parses_file(self, mock_open):
    """Verify config file parsing."""
    # Arrange
    mock_open.return_value.__enter__.return_value.read.return_value = (
        '{"key": "value"}'
    )

    # Act
    config = read_config("config.json")

    # Assert
    assert config["key"] == "value"
```

---

## Async Test Templates

### Async Function Tests

```python
"""
Tests for async functions.
"""
import pytest

from features.async_service import fetch_data, AsyncDataService


class TestAsyncFunctions:
    """Tests for async functions."""

    @pytest.mark.asyncio
    async def test_fetch_data_returns_result(self):
        """Verify async fetch returns data."""
        # Arrange
        url = "https://api.example.com/data"

        # Act
        result = await fetch_data(url)

        # Assert
        assert result is not None
        assert "data" in result

    @pytest.mark.asyncio
    async def test_fetch_data_timeout_raises_error(self):
        """Verify timeout handling."""
        # Arrange
        url = "https://slow.example.com/data"

        # Act & Assert
        with pytest.raises(TimeoutError):
            await fetch_data(url, timeout=0.001)


class TestAsyncDataService:
    """Tests for async service class."""

    @pytest.fixture
    async def service(self):
        """Create async service instance."""
        service = AsyncDataService()
        await service.connect()
        yield service
        await service.disconnect()

    @pytest.mark.asyncio
    async def test_service_query_returns_results(self, service):
        """Verify async query execution."""
        # Arrange
        query = "SELECT * FROM items"

        # Act
        results = await service.query(query)

        # Assert
        assert isinstance(results, list)
```

### Async Mock Testing

```python
@pytest.mark.asyncio
async def test_async_service_with_mock(self):
    """Test async function with mocked dependency."""
    # Arrange
    mock_client = AsyncMock()
    mock_client.fetch.return_value = {"data": "value"}
    service = AsyncService(client=mock_client)

    # Act
    result = await service.get_data()

    # Assert
    mock_client.fetch.assert_awaited_once()
    assert result["data"] == "value"
```

---

## Test Naming Conventions

### Pattern

```
test_<unit>_<scenario>_<expected_result>
```

### Examples

| Test Name | What It Tests |
|-----------|---------------|
| `test_calculate_total_with_empty_list_returns_zero` | Empty input edge case |
| `test_validate_email_with_invalid_format_returns_false` | Validation failure |
| `test_save_user_with_duplicate_email_raises_error` | Exception case |
| `test_parse_date_with_iso_format_returns_datetime` | Happy path |
| `test_fetch_data_when_api_unavailable_retries_three_times` | Retry behavior |

### Class Naming

```python
class TestClassName:           # For class tests
class TestFunctionName:        # For function tests  
class TestFeatureIntegration:  # For integration tests
class TestUserWorkflowE2E:     # For E2E tests
```

---

## Test Markers

### Common Markers

```python
# Mark slow tests
@pytest.mark.slow
def test_large_dataset_processing():
    ...

# Mark tests requiring network
@pytest.mark.network
def test_api_integration():
    ...

# Mark tests requiring database
@pytest.mark.database
def test_database_operations():
    ...

# Skip test conditionally
@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_specific_feature():
    ...

# Expected failure
@pytest.mark.xfail(reason="Known bug, fix pending")
def test_broken_feature():
    ...
```

### Configure in pytest.ini

```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    network: marks tests requiring network access
    database: marks tests requiring database
    e2e: marks end-to-end tests
```

---

## Checklist Before Committing Tests

- [ ] Test names follow `test_<unit>_<scenario>_<expected>` pattern
- [ ] Each test has Arrange-Act-Assert structure
- [ ] Tests are independent (no shared state)
- [ ] Fixtures clean up after themselves
- [ ] Edge cases covered (empty, null, boundary values)
- [ ] Exception cases tested with `pytest.raises`
- [ ] Mocks verify correct interactions
- [ ] No hardcoded paths (use `tmp_path` fixture)
- [ ] Tests run in isolation (`pytest <test_file>`)
- [ ] Tests run fast (< 1 second for unit tests)

---

*Template Version: 1.0 | Last Updated: 2025-11-27*
