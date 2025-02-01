"""Git management for Python Release Master."""

import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

from python_release_master.core.errors import ReleaseError, ErrorCode
from python_release_master.core.logger import logger


class GitManager:
    """Manages Git operations."""
    
    def __init__(self, workspace_dir: Path):
        """Initialize Git manager.
        
        Args:
            workspace_dir: Path to workspace directory
        """
        self.workspace_dir = workspace_dir
    
    def validate_git_installed(self) -> None:
        """Validate that Git is installed.
        
        Raises:
            ReleaseError: If Git is not installed
        """
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ReleaseError(
                ErrorCode.GIT_NOT_INSTALLED,
                "Git is not installed",
                context={"command": "git --version"}
            )
    
    def validate_git_repo(self) -> None:
        """Validate that current directory is a Git repository.
        
        Raises:
            ReleaseError: If not a Git repository
        """
        git_dir = self.workspace_dir / ".git"
        if not git_dir.exists():
            raise ReleaseError(
                ErrorCode.GIT_REPO_NOT_FOUND,
                "Git repository not found",
                context={"directory": str(self.workspace_dir)}
            )
    
    def get_changed_files(self) -> List[str]:
        """Get list of files that have changes in Git.
        
        Returns:
            List of changed file paths
        """
        changes = []
        
        try:
            # Get staged changes
            staged = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                check=True, capture_output=True, text=True
            ).stdout.strip().split("\n")
            if staged and staged[0]:
                changes.extend(staged)
            
            # Get unstaged changes
            unstaged = subprocess.run(
                ["git", "diff", "--name-only"],
                check=True, capture_output=True, text=True
            ).stdout.strip().split("\n")
            if unstaged and unstaged[0]:
                changes.extend(unstaged)
            
            # Get untracked files
            untracked = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                check=True, capture_output=True, text=True
            ).stdout.strip().split("\n")
            if untracked and untracked[0]:
                changes.extend(untracked)
            
            return sorted(list(set(changes)))
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to get Git changed files: {e}")
            return []
    
    def commit_changes(self, message: str) -> None:
        """Commit changes to Git.
        
        Args:
            message: Commit message
            
        Raises:
            ReleaseError: If commit fails
        """
        try:
            # Stage all changes
            subprocess.run(
                ["git", "add", "."],
                check=True, capture_output=True, text=True
            )
            
            # Create commit
            subprocess.run(
                ["git", "commit", "-m", message],
                check=True, capture_output=True, text=True
            )
            
            logger.success(f"Created commit: {message}")
        except subprocess.CalledProcessError as e:
            raise ReleaseError(
                ErrorCode.GIT_COMMIT_FAILED,
                f"Failed to commit changes: {e.stderr}",
                context={"message": message}
            )
    
    def create_tag(self, tag: str, message: str) -> None:
        """Create an annotated Git tag.
        
        Args:
            tag: Tag name
            message: Tag message
            
        Raises:
            ReleaseError: If tag creation fails
        """
        try:
            subprocess.run(
                ["git", "tag", "-a", tag, "-m", message],
                check=True, capture_output=True, text=True
            )
            logger.success(f"Created Git tag {tag}")
        except subprocess.CalledProcessError as e:
            raise ReleaseError(
                ErrorCode.GIT_TAG_FAILED,
                f"Failed to create Git tag: {e.stderr}",
                context={"tag": tag, "message": message}
            )
    
    def push_changes(self, tags: bool = False) -> None:
        """Push changes to remote.
        
        Args:
            tags: Whether to push tags
            
        Raises:
            ReleaseError: If push fails
        """
        try:
            # Push commits
            subprocess.run(
                ["git", "push", "origin", "HEAD"],
                check=True, capture_output=True, text=True
            )
            logger.success("Pushed changes to remote")
            
            # Push tags if requested
            if tags:
                subprocess.run(
                    ["git", "push", "--tags"],
                    check=True, capture_output=True, text=True
                )
                logger.success("Pushed tags to remote")
        except subprocess.CalledProcessError as e:
            raise ReleaseError(
                ErrorCode.GIT_PUSH_FAILED,
                f"Failed to push changes: {e.stderr}",
                context={"tags": tags}
            )
    
    def create_release(self, tag: str, title: str, description: str, draft: bool = False,
                      prerelease: bool = False, generate_notes: bool = True) -> None:
        """Create a GitHub release.
        
        Args:
            tag: Tag name
            title: Release title
            description: Release description
            draft: Whether to create as draft
            prerelease: Whether to mark as prerelease
            generate_notes: Whether to auto-generate release notes
            
        Raises:
            ReleaseError: If release creation fails
        """
        try:
            cmd = [
                "gh", "release", "create",
                tag,
                "--title", title,
                "--notes", description,
            ]
            
            if draft:
                cmd.append("--draft")
            if prerelease:
                cmd.append("--prerelease")
            if generate_notes:
                cmd.append("--generate-notes")
            
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.success("GitHub release created successfully")
        except subprocess.CalledProcessError as e:
            raise ReleaseError(
                ErrorCode.GIT_RELEASE_FAILED,
                f"Failed to create GitHub release: {e.stderr}",
                context={
                    "tag": tag,
                    "title": title,
                    "draft": draft,
                    "prerelease": prerelease
                }
            ) 