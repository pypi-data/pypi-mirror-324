"""Package verification utilities."""

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
            
            # Create test files
            dockerfile_path = temp_path / "Dockerfile"
            dockerfile_path.write_text(DOCKERFILE_TEMPLATE)
            
            config_path = temp_path / "test-config.yml"
            config_path.write_text(TEST_CONFIG_TEMPLATE)
            
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