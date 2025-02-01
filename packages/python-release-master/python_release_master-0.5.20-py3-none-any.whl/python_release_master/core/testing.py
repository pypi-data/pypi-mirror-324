"""Test execution utilities for Python Release Master."""

import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

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


"""Testing utilities for Python Release Master."""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import Tuple

from rich.console import Console

console = Console()

DOCKERFILE_TEMPLATE = """
FROM python:3.9-slim

WORKDIR /test
RUN apt-get update && apt-get install -y git

# Create test repository
RUN git init test-repo && cd test-repo && \
    git config --global user.email "test@example.com" && \
    git config --global user.name "Test User" && \
    echo "# Test Repository" > README.md && \
    git add README.md && \
    git commit -m "Initial commit"

# Install package
COPY dist/* /tmp/
RUN pip install /tmp/*.whl

# Copy test config
COPY test-config.yml /test/test-repo/python-release-master.yml

# Run test command
WORKDIR /test/test-repo
CMD ["python", "-m", "python_release_master", "release", "create", "--version-bump", "patch", "--ai=false", "--push=false", "--publish=false"]
"""

TEST_CONFIG_TEMPLATE = """
version_files:
  - README.md
ai:
  enabled: false
git:
  push: false
pypi:
  publish: false
"""

def create_test_dockerfile(temp_dir: Path) -> None:
    """Create Dockerfile and test config in temporary directory.
    
    Args:
        temp_dir: Path to temporary directory
    """
    # Write Dockerfile
    dockerfile_path = temp_dir / "Dockerfile"
    dockerfile_path.write_text(DOCKERFILE_TEMPLATE)
    
    # Write test config
    config_path = temp_dir / "test-config.yml"
    config_path.write_text(TEST_CONFIG_TEMPLATE)

def verify_current_package() -> Tuple[bool, str]:
    """Verify the current package version in a clean Docker environment.
    
    Returns:
        Tuple of (success, message)
    """
    try:
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Copy dist files
            dist_path = Path("dist")
            if not dist_path.exists() or not list(dist_path.glob("*.whl")):
                return False, "No wheel file found in dist directory. Run build first."
                
            os.system(f"cp -r {dist_path}/* {temp_path}/")
            
            # Create Dockerfile and config
            create_test_dockerfile(temp_path)
            
            # Build and run Docker image
            image_name = "python-release-master-test"
            subprocess.run(
                ["docker", "build", "-t", image_name, "."],
                cwd=temp_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            result = subprocess.run(
                ["docker", "run", "--rm", image_name],
                cwd=temp_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return False, f"Test failed:\n{result.stdout}\n{result.stderr}"
            
            return True, "Package verification successful"
            
    except subprocess.CalledProcessError as e:
        return False, f"Docker error:\n{e.stdout}\n{e.stderr}"
    except Exception as e:
        return False, str(e)

def verify_package_version(version: str) -> Tuple[bool, str]:
    """Verify a specific version of the package.
    
    Args:
        version: Version to verify (e.g. "0.1.0")
        
    Returns:
        Tuple of (success, output)
    """
    package_spec = f"python-release-master=={version}"
    return run_docker_test(package_spec)

def verify_package_wheel(wheel_path: str) -> Tuple[bool, str]:
    """Verify a package wheel file.
    
    Args:
        wheel_path: Path to the wheel file
        
    Returns:
        Tuple of (success, output)
    """
    return run_docker_test(wheel_path)

def run_docker_test(package_spec: str, timeout: int = 300) -> Tuple[bool, str]:
    """Run package test in Docker container.
    
    Args:
        package_spec: Package specification (e.g. package_name==version or path to wheel)
        timeout: Maximum time to wait for container execution in seconds
        
    Returns:
        Tuple of (success, output)
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        dockerfile_path = create_test_dockerfile(temp_path)
        
        # Build Docker image
        image_name = "python-release-master-test"
        try:
            subprocess.run(
                ["docker", "build", "-t", image_name, "-f", str(dockerfile_path), temp_dir],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            return False, f"Failed to build Docker image:\n{e.stdout}\n{e.stderr}"
        
        # Run container
        try:
            result = subprocess.run(
                ["docker", "run", "--rm", image_name],
                check=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, f"Container execution failed:\n{e.stdout}\n{e.stderr}"
        except subprocess.TimeoutExpired:
            return False, f"Container execution timed out after {timeout} seconds"
        finally:
            # Cleanup
            try:
                subprocess.run(["docker", "rmi", "-f", image_name], capture_output=True)
            except:
                pass 