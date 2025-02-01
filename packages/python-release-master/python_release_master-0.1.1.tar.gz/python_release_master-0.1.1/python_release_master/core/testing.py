"""Testing functionality for python-release-master."""
from typing import List, Optional, Tuple
import os
import subprocess
from .config import Config


class TestError(Exception):
    """Custom exception for test failures."""


def run_unit_tests(test_path: str = "tests/unit") -> Tuple[bool, str]:
    """Run unit tests specifically."""
    cmd = ["pytest", test_path, "-v"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stdout if e.stdout else str(e)


def run_integration_tests(test_path: str = "tests/integration") -> Tuple[bool, str]:
    """Run integration tests specifically."""
    cmd = ["pytest", test_path, "-v"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stdout if e.stdout else str(e)


def run_docker_tests() -> Tuple[bool, str]:
    """Run tests in a Docker container."""
    try:
        # Build the test image
        build = subprocess.run(
            ["docker", "build", "-t", "python-release-master-test", "."],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Run tests in container
        test = subprocess.run(
            ["docker", "run", "--rm", "python-release-master-test", "pytest", "-v"],
            capture_output=True,
            text=True,
            check=True
        )
        
        return True, test.stdout
    except subprocess.CalledProcessError as e:
        raise TestError("Docker tests failed")


def run_tests(config: Config) -> None:
    """Run all test suites with coverage."""
    try:
        # Run tests with coverage
        cmd = ["pytest"]
        
        # Add coverage options if not in skip_steps
        if "coverage" not in config.skip_steps:
            cmd.extend(["--cov", "--cov-report=term-missing"])
        
        # Add test directory
        cmd.append("tests/")
        
        # Run the tests
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.returncode != 0:
            raise TestError("Unit tests failed")
    except subprocess.CalledProcessError as e:
        raise TestError("Unit tests failed")
    except Exception as e:
        raise TestError(f"Unexpected error during tests: {str(e)}")


def run_linting() -> bool:
    """Run code quality checks (flake8, black, isort)."""
    try:
        # Run flake8
        subprocess.run(["flake8", "."], check=True)
        
        # Run black in check mode
        subprocess.run(["black", "--check", "."], check=True)
        
        # Run isort in check mode
        subprocess.run(["isort", "--check-only", "."], check=True)
        
        return True
    except subprocess.CalledProcessError:
        return False


def run_type_checking() -> bool:
    """Run mypy type checking."""
    try:
        subprocess.run(["mypy", "."], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def run_all_checks(config: Config) -> bool:
    """Run all tests, linting, and type checking based on configuration."""
    try:
        run_tests(config)
        if "lint" not in config.skip_steps:
            if not run_linting():
                return False
        if "type" not in config.skip_steps:
            if not run_type_checking():
                return False
        return True
    except TestError:
        return False 