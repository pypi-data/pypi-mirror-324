"""Test execution utilities for Python Release Master."""

import subprocess
from pathlib import Path
from typing import List, Optional

from rich.console import Console

from python_release_master.core.config import Config

console = Console()


def run_tests(config: Config) -> None:
    """Run all test suites."""
    try:
        run_unit_tests()
        run_integration_tests()
        run_docker_tests()
    except TestError as e:
        raise ValueError(f"Test execution failed: {str(e)}")


def run_unit_tests() -> None:
    """Run unit tests using pytest."""
    console.print("Running unit tests...")
    
    if not Path("tests").exists():
        console.print("[yellow]No tests directory found, skipping unit tests[/yellow]")
        return
    
    try:
        subprocess.run(
            ["pytest", "-v", "--cov"],
            check=True,
            capture_output=True,
            text=True,
        )
        console.print("[green]Unit tests passed successfully[/green]")
    except subprocess.CalledProcessError as e:
        raise TestError(f"Unit tests failed:\n{e.stdout}\n{e.stderr}")


def run_integration_tests() -> None:
    """Run integration tests if available."""
    console.print("Running integration tests...")
    
    integration_dir = Path("tests/integration")
    if not integration_dir.exists():
        console.print("[yellow]No integration tests found, skipping[/yellow]")
        return
    
    try:
        subprocess.run(
            ["pytest", "-v", "tests/integration"],
            check=True,
            capture_output=True,
            text=True,
        )
        console.print("[green]Integration tests passed successfully[/green]")
    except subprocess.CalledProcessError as e:
        raise TestError(f"Integration tests failed:\n{e.stdout}\n{e.stderr}")


def run_docker_tests() -> None:
    """Run Docker-based tests if available."""
    console.print("Running Docker tests...")
    
    dockerfile = Path("Dockerfile.test")
    if not dockerfile.exists():
        console.print("[yellow]No Dockerfile.test found, skipping Docker tests[/yellow]")
        return
    
    try:
        # Build test image
        subprocess.run(
            ["docker", "build", "-f", "Dockerfile.test", "-t", "package-test", "."],
            check=True,
            capture_output=True,
            text=True,
        )
        
        # Run tests in container
        subprocess.run(
            ["docker", "run", "--rm", "package-test"],
            check=True,
            capture_output=True,
            text=True,
        )
        
        console.print("[green]Docker tests passed successfully[/green]")
    except subprocess.CalledProcessError as e:
        raise TestError(f"Docker tests failed:\n{e.stdout}\n{e.stderr}")


class TestError(Exception):
    """Custom exception for test failures."""

    pass 