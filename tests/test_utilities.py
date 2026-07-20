"""Tests for sjamal_utilities."""

import os
import tempfile
import unittest
from pathlib import Path

from sjamal_utilities.env_validator import EnvValidator
from sjamal_utilities.file_utils import FileUtils
from sjamal_utilities.config_loader import ConfigLoader
from sjamal_utilities.logger_setup import setup_logging
from sjamal_utilities.retry_decorator import retry


class TestEnvValidator(unittest.TestCase):
    """Test environment variable validation."""

    def test_check_all_valid(self):
        """Test with all vars present."""
        os.environ["TEST_VAR_1"] = "value1"
        os.environ["TEST_VAR_2"] = "value2"

        result = EnvValidator.check(["TEST_VAR_1", "TEST_VAR_2"], strict=False)
        assert result["valid"] == ["TEST_VAR_1", "TEST_VAR_2"]
        assert result["missing"] == []
        assert result["empty"] == []

    def test_check_missing_raises(self):
        """Test that missing vars raise in strict mode."""
        with self.assertRaises(ValueError):
            EnvValidator.check(["NONEXISTENT_VAR_XYZ"], strict=True)

    def test_check_empty_raises(self):
        """Test that empty vars raise in strict mode."""
        os.environ["EMPTY_VAR"] = ""
        with self.assertRaises(ValueError):
            EnvValidator.check(["EMPTY_VAR"], strict=True)


class TestFileUtils(unittest.TestCase):
    """Test file utilities."""

    def setUp(self):
        """Create temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def test_write_and_read(self):
        """Test writing and reading files."""
        filepath = Path(self.temp_dir) / "test.txt"
        content = "Hello, World!"

        FileUtils.write_file(filepath, content)
        read_content = FileUtils.read_file(filepath)

        assert read_content == content

    def test_atomic_write(self):
        """Test atomic write."""
        filepath = Path(self.temp_dir) / "atomic.txt"
        content = "Atomic content"

        FileUtils.atomic_write(filepath, content)
        assert FileUtils.read_file(filepath) == content

    def test_checksum(self):
        """Test checksum calculation."""
        filepath = Path(self.temp_dir) / "checksum_test.txt"
        content = "Test content"

        FileUtils.write_file(filepath, content)
        checksum1 = FileUtils.checksum(filepath, algorithm="sha256")
        checksum2 = FileUtils.checksum(filepath, algorithm="sha256")

        assert checksum1 == checksum2
        assert len(checksum1) == 64  # SHA256 is 64 hex chars

    def test_walk_tree(self):
        """Test directory tree walking."""
        base = Path(self.temp_dir)
        (base / "subdir").mkdir()

        FileUtils.write_file(base / "file1.txt", "content1")
        FileUtils.write_file(base / "subdir" / "file2.py", "content2")

        files = FileUtils.walk_tree(base)
        assert len(files) >= 2

        py_files = FileUtils.walk_tree(base, pattern="*.py")
        assert len(py_files) >= 1


class TestConfigLoader(unittest.TestCase):
    """Test configuration loading."""

    def setUp(self):
        """Create temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def test_load_json(self):
        """Test loading JSON config."""
        config_path = Path(self.temp_dir) / "config.json"
        config_path.write_text('{"key": "value", "number": 42}')

        config = ConfigLoader.load_json(config_path)
        assert config["key"] == "value"
        assert config["number"] == 42

    def test_load_env(self):
        """Test loading .env file."""
        env_path = Path(self.temp_dir) / ".env"
        env_path.write_text("KEY1=value1\nKEY2=value2\n# Comment\n")

        env_vars = ConfigLoader.load_env(env_path)
        assert env_vars["KEY1"] == "value1"
        assert env_vars["KEY2"] == "value2"

    def test_merge(self):
        """Test config merging."""
        base = {"a": 1, "b": {"c": 2}}
        override = {"b": {"d": 3}, "e": 4}

        merged = ConfigLoader.merge(base, override)
        assert merged["a"] == 1
        assert merged["b"]["c"] == 2
        assert merged["b"]["d"] == 3
        assert merged["e"] == 4


class TestRetryDecorator(unittest.TestCase):
    """Test retry decorator."""

    def test_retry_success_first_attempt(self):
        """Test function succeeds on first attempt."""

        @retry(max_attempts=3)
        def always_succeeds():
            return "success"

        result = always_succeeds()
        assert result == "success"

    def test_retry_eventual_success(self):
        """Test function succeeds after retries."""
        attempts = {"count": 0}

        @retry(max_attempts=3, delay=0.01)
        def fails_twice():
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise ValueError("Not yet")
            return "success"

        result = fails_twice()
        assert result == "success"
        assert attempts["count"] == 3

    def test_retry_max_attempts_exceeded(self):
        """Test that max attempts are respected."""
        attempts = {"count": 0}

        @retry(max_attempts=2, delay=0.01)
        def always_fails():
            attempts["count"] += 1
            raise ValueError("Always fails")

        with self.assertRaises(ValueError):
            always_fails()

        assert attempts["count"] == 2


class TestLoggingSetup(unittest.TestCase):
    """Test logging setup."""

    def test_logger_creation(self):
        """Test that logger is created and configured."""
        logger = setup_logging(name="test_logger")
        assert logger.name == "test_logger"
        assert len(logger.handlers) > 0


if __name__ == "__main__":
    unittest.main()
