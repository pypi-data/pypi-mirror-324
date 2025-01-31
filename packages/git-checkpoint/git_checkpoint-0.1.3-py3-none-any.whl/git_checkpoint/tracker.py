"""
Implementation of the CheckpointTracker class.
Handles Git-based workspace state management.
"""

import json
import shutil
import tempfile
import time
from pathlib import Path
from typing import List, Optional

import git
from git import Repo
from git.exc import GitCommandError

from .interface import (
    CheckpointConfig,
    CheckpointError,
    CheckpointMetadata,
    CheckpointNotFoundError,
    CheckpointTracker,
    DiffInfo,
    GitError,
    WorkspaceError,
)


class CheckpointTrackerImpl(CheckpointTracker):
    """Implementation of the CheckpointTracker interface."""

    # Class constants
    DEFAULT_METADATA_FILENAME: str = "checkpoint.meta.json"
    DEFAULT_CHECKPOINT_DIR: str = "git_checkpoints"

    def __init__(
        self,
        task_id: str,
        workspace_path: str,
        config: Optional[CheckpointConfig] = None,
    ):
        """Initialize a new checkpoint tracker."""
        self.task_id = task_id
        self.workspace_path = Path(workspace_path)
        self.config = config or CheckpointConfig()
        self._repo: Optional[Repo] = None
        self._shadow_git_path: Optional[Path] = None
        self.last_commit_hash: Optional[str] = None
        self._validate_workspace()

    @classmethod
    def create(
        cls,
        task_id: str,
        workspace_path: str,
        config: Optional[CheckpointConfig] = None,
    ) -> "CheckpointTrackerImpl":
        """Create and initialize a new checkpoint tracker."""
        tracker = cls(task_id, workspace_path, config)
        tracker.init_shadow_git()
        return tracker

    def init_shadow_git(self) -> str:
        """Initialize shadow git repository for tracking workspace state."""
        try:
            # Create shadow git directory in system temp with task ID
            temp_dir = Path(tempfile.gettempdir()) / self.DEFAULT_CHECKPOINT_DIR
            self._shadow_git_path = temp_dir / self.task_id
            self._shadow_git_path.mkdir(parents=True, exist_ok=True)

            # Initialize git repo
            self._repo = Repo.init(self._shadow_git_path)

            # Configure git
            with self._repo.config_writer() as git_config:
                git_config.set_value("user", "name", "GitCheckpoint")
                git_config.set_value("user", "email", "checkpoint@git-checkpoint.dev")
                git_config.set_value("core", "autocrlf", "input")

            # Copy workspace contents to shadow repo
            self._sync_workspace_to_shadow()

            # Initial commit
            self._repo.git.add(A=True)  # Stage all files including untracked
            commit = self._repo.index.commit("Initial checkpoint")
            self.last_commit_hash = commit.hexsha

            return str(self._shadow_git_path)

        except (OSError, GitCommandError) as e:
            raise GitError(f"Failed to initialize shadow git repo: {str(e)}")

    def commit(self) -> Optional[str]:
        """Create a new checkpoint of current workspace state."""
        if not self._repo:
            raise GitError("Shadow git repository not initialized")

        try:
            # Sync latest workspace state
            self._sync_workspace_to_shadow()

            # Stage all changes including untracked files
            self._repo.git.add(A=True)

            # Check for changes
            if not (self._repo.is_dirty(untracked_files=True) or self._repo.untracked_files):
                return None

            # Commit changes
            commit = self._repo.index.commit("Checkpoint")
            self.last_commit_hash = commit.hexsha
            return commit.hexsha

        except GitCommandError as e:
            raise GitError(f"Failed to create checkpoint: {str(e)}")

    def _sync_workspace_to_shadow(self) -> None:
        """Sync workspace contents to shadow git repo."""
        if not self._shadow_git_path:
            raise GitError("Shadow git path not initialized")

        try:
            # Clear shadow git repo except .git directory
            for item in self._shadow_git_path.iterdir():
                if item.name != ".git":
                    if item.is_file():
                        item.unlink()
                    else:
                        shutil.rmtree(item)

            # Copy workspace contents
            for item in self.workspace_path.iterdir():
                # Convert to relative path for pattern matching
                rel_path = item.relative_to(self.workspace_path)
                if self._should_track_path(rel_path):
                    dest = self._shadow_git_path / item.name
                    if item.is_file():
                        shutil.copy2(item, dest)
                    else:
                        shutil.copytree(item, dest, dirs_exist_ok=True)

        except OSError as e:
            raise WorkspaceError(f"Failed to sync workspace: {str(e)}")

    def _should_track_path(self, path: Path) -> bool:
        """Check if a path should be tracked based on config."""
        # Skip .git directories
        if ".git" in path.parts:
            return False

        # Check ignore patterns
        if self.config.ignore_patterns:
            for pattern in self.config.ignore_patterns:
                if path.match(pattern):
                    return False

        return True

    def _validate_workspace(self) -> None:
        """Validate workspace path."""
        if not self.workspace_path.exists():
            raise WorkspaceError(f"Workspace path does not exist: {self.workspace_path}")

        if not self.workspace_path.is_dir():
            raise WorkspaceError(f"Workspace path is not a directory: {self.workspace_path}")

        # Check if path is in protected directories
        protected = [
            Path.home(),
            Path.home() / "Desktop",
            Path.home() / "Documents",
            Path.home() / "Downloads",
        ]
        if any(
            self.workspace_path == p or self.workspace_path.is_relative_to(p) for p in protected
        ):
            raise WorkspaceError(f"Workspace path is in protected directory: {self.workspace_path}")

    def cleanup(self) -> None:
        """Clean up shadow git repository."""
        if self._shadow_git_path and self._shadow_git_path.exists():
            try:
                shutil.rmtree(self._shadow_git_path)
            except OSError as e:
                raise GitError(f"Failed to cleanup shadow git repo: {str(e)}")

    def reset_head(self, commit_hash: str) -> None:
        """Reset workspace to a specific checkpoint."""
        if not self._repo:
            raise GitError("Shadow git repository not initialized")

        try:
            # Verify commit exists
            try:
                self._repo.commit(commit_hash)
            except (ValueError, git.exc.BadName):
                raise GitError(f"Invalid commit hash: {commit_hash}")

            # Reset to commit
            self._repo.head.reset(commit=commit_hash, working_tree=True)
            self.last_commit_hash = commit_hash

            # Sync shadow repo back to workspace
            self._sync_shadow_to_workspace()

        except GitCommandError as e:
            raise GitError(f"Failed to reset to checkpoint: {str(e)}")

    def get_diff_set(
        self, lhs_hash: Optional[str] = None, rhs_hash: Optional[str] = None
    ) -> List[DiffInfo]:
        """Get differences between two checkpoints."""
        if not self._repo:
            raise GitError("Shadow git repository not initialized")

        try:
            # Default to comparing with HEAD if rhs_hash not provided
            if not rhs_hash:
                rhs_hash = self._repo.head.commit.hexsha

            # Default to comparing with parent if lhs_hash not provided
            if not lhs_hash:
                try:
                    lhs_hash = self._repo.commit(rhs_hash).parents[0].hexsha
                except IndexError:
                    # No parent commit, comparing with empty state
                    lhs_hash = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"  # git empty tree

            # Stage all files to get accurate status
            self._repo.git.add(A=True)

            # Get diff between commits using git diff command
            diffs = self._repo.git.diff(
                lhs_hash,
                rhs_hash,
                "--name-status",  # Get file status (modified, added, deleted)
                "--find-renames",  # Detect renamed files
                "--ignore-blank-lines",
                "--ignore-space-at-eol",
                "--no-renames",  # Don't detect renames to get accurate add/delete
            ).splitlines()

            # Convert to DiffInfo objects
            diff_infos: List[DiffInfo] = []
            for diff_line in diffs:
                if not diff_line:
                    continue

                # Parse diff line (format: "status\tpath")
                parts = diff_line.split("\t")
                if len(parts) < 2:
                    continue

                status = parts[0]
                path = parts[1]

                # Skip ignored files
                if not self._should_track_path(Path(path)):
                    continue

                if status == "A":  # Added file
                    diff_infos.append(
                        DiffInfo(
                            relative_path=path,
                            absolute_path=str(self.workspace_path / path),
                            before="",
                            after=self._get_file_content_at_commit(path, rhs_hash),
                        )
                    )
                elif status == "D":  # Deleted file
                    diff_infos.append(
                        DiffInfo(
                            relative_path=path,
                            absolute_path=str(self.workspace_path / path),
                            before=self._get_file_content_at_commit(path, lhs_hash),
                            after="",
                        )
                    )
                elif status == "M":  # Modified file
                    diff_infos.append(
                        DiffInfo(
                            relative_path=path,
                            absolute_path=str(self.workspace_path / path),
                            before=self._get_file_content_at_commit(path, lhs_hash),
                            after=self._get_file_content_at_commit(path, rhs_hash),
                        )
                    )

            # If comparing with empty tree, add all files as new
            if lhs_hash == "4b825dc642cb6eb9a060e54bf8d69288fbee4904":
                # Get all files in the commit
                files = self._repo.git.ls_tree(
                    "-r",  # Recursive
                    "--name-only",  # Only show file names
                    rhs_hash,
                ).splitlines()

                # Add each file as new
                for path in files:
                    if not self._should_track_path(Path(path)):
                        continue
                    if not any(d.relative_path == path for d in diff_infos):
                        diff_infos.append(
                            DiffInfo(
                                relative_path=path,
                                absolute_path=str(self.workspace_path / path),
                                before="",
                                after=self._get_file_content_at_commit(path, rhs_hash),
                            )
                        )

            # Get untracked files if comparing with HEAD
            if rhs_hash == self._repo.head.commit.hexsha:
                for path in self._repo.untracked_files:
                    if self._should_track_path(Path(path)):
                        with open(self._shadow_git_path / path) as f:
                            content = f.read()
                        diff_infos.append(
                            DiffInfo(
                                relative_path=path,
                                absolute_path=str(self.workspace_path / path),
                                before="",
                                after=content,
                            )
                        )

            return diff_infos

        except (GitCommandError, ValueError, OSError) as e:
            raise GitError(f"Failed to get diff: {str(e)}")

    def _get_file_content_at_commit(self, path: str, commit_hash: str) -> str:
        """Get the content of a file at a specific commit."""
        try:
            blob = self._repo.commit(commit_hash).tree / path
            return blob.data_stream.read().decode("utf-8")
        except (KeyError, AttributeError):
            return ""

    def _sync_shadow_to_workspace(self) -> None:
        """Sync shadow git repo contents back to workspace."""
        if not self._shadow_git_path:
            raise GitError("Shadow git path not initialized")

        try:
            # Clear workspace except .git and ignored files
            for item in self.workspace_path.iterdir():
                if self._should_track_path(item.relative_to(self.workspace_path)):
                    if item.is_file():
                        item.unlink()
                    else:
                        shutil.rmtree(item)

            # Copy shadow contents to workspace
            for item in self._shadow_git_path.iterdir():
                if item.name != ".git":
                    dest = self.workspace_path / item.name
                    if item.is_file():
                        shutil.copy2(item, dest)
                    else:
                        shutil.copytree(item, dest, dirs_exist_ok=True)

        except OSError as e:
            raise WorkspaceError(f"Failed to sync workspace: {str(e)}")

    def save_metadata(self) -> None:
        """Save checkpoint metadata to disk."""
        if not self._shadow_git_path:
            raise GitError("Shadow git path not initialized")

        try:
            metadata = self.get_metadata()
            metadata_path = self._shadow_git_path / self.DEFAULT_METADATA_FILENAME

            # Convert to dict, handling Path objects
            metadata_dict = {
                "task_id": metadata.task_id,
                "workspace_path": str(metadata.workspace_path),
                "last_commit_hash": metadata.last_commit_hash,
                "created_at": metadata.created_at,
                "config": {
                    "enabled": metadata.config.enabled,
                    "storage_path": (
                        str(metadata.config.storage_path) if metadata.config.storage_path else None
                    ),
                    "ignore_patterns": metadata.config.ignore_patterns,
                },
            }

            with open(metadata_path, "w") as f:
                json.dump(metadata_dict, f, indent=2)

        except (OSError, TypeError) as e:
            raise CheckpointError(f"Failed to save metadata: {str(e)}")

    @classmethod
    def load(cls, task_id: str, storage_path: Optional[Path] = None) -> "CheckpointTrackerImpl":
        """Load an existing checkpoint tracker from storage."""
        try:
            # Find metadata file
            temp_dir = Path(tempfile.gettempdir()) / cls.DEFAULT_CHECKPOINT_DIR
            shadow_path = temp_dir / task_id
            metadata_path = shadow_path / cls.DEFAULT_METADATA_FILENAME

            if not metadata_path.exists():
                raise CheckpointNotFoundError(f"No checkpoint found for task: {task_id}")

            # Load metadata
            with open(metadata_path) as f:
                metadata_dict = json.load(f)

            # Create config
            config = CheckpointConfig(
                enabled=metadata_dict["config"]["enabled"],
                storage_path=(
                    Path(metadata_dict["config"]["storage_path"])
                    if metadata_dict["config"]["storage_path"]
                    else None
                ),
                ignore_patterns=metadata_dict["config"]["ignore_patterns"],
            )

            # Create tracker instance
            tracker = cls(
                task_id=metadata_dict["task_id"],
                workspace_path=metadata_dict["workspace_path"],
                config=config,
            )

            # Set loaded state
            tracker._shadow_git_path = shadow_path
            tracker._repo = Repo(shadow_path)
            tracker.last_commit_hash = metadata_dict["last_commit_hash"]

            return tracker

        except (OSError, json.JSONDecodeError) as e:
            raise CheckpointError(f"Failed to load checkpoint: {str(e)}")

    def get_metadata(self) -> CheckpointMetadata:
        """Get metadata about the current checkpoint state."""
        return CheckpointMetadata(
            task_id=self.task_id,
            workspace_path=self.workspace_path,
            last_commit_hash=self.last_commit_hash,
            created_at=time.time(),
            config=self.config,
        )
