"""
Core interface definitions for the checkpoint system.
Provides the main types and classes for managing workspace checkpoints.
"""

import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional


class CheckpointError(Exception):
    """Base exception class for checkpoint-related errors."""

    pass


class WorkspaceError(CheckpointError):
    """Raised when there are workspace validation or access issues."""

    pass


class GitError(CheckpointError):
    """Raised when git operations fail."""

    pass


class CheckpointNotFoundError(CheckpointError):
    """Raised when trying to load a non-existent checkpoint."""

    pass


@dataclass
class DiffInfo:
    """Information about changes between two states."""

    relative_path: str
    absolute_path: str
    before: str
    after: str


class RestoreType(Enum):
    """Types of checkpoint restoration."""

    TASK = "task"  # Restore just the task state
    WORKSPACE = "workspace"  # Restore just the workspace files
    TASK_AND_WORKSPACE = "taskAndWorkspace"  # Restore both


@dataclass
class CheckpointConfig:
    """Configuration for checkpoint behavior."""

    enabled: bool = True
    storage_path: Optional[Path] = None
    ignore_patterns: List[str] = None

    def __post_init__(self):
        if self.ignore_patterns is None:
            self.ignore_patterns = []


@dataclass
class CheckpointMetadata:
    """Metadata about a checkpoint."""

    task_id: str
    workspace_path: Path
    last_commit_hash: Optional[str]
    created_at: float  # Unix timestamp
    config: CheckpointConfig


class CheckpointTracker:
    """
    Main interface for managing workspace checkpoints.
    Uses Git under the hood for state management.
    """

    # Class constants
    DEFAULT_METADATA_FILENAME: ClassVar[str] = "checkpoint.meta.json"

    def __init__(
        self,
        task_id: str,
        workspace_path: str,
        config: Optional[CheckpointConfig] = None,
    ):
        """
        Initialize a new checkpoint tracker.

        Args:
            task_id: Unique identifier for the task
            workspace_path: Path to the workspace to track
            config: Optional configuration settings
        """
        self.task_id = task_id
        self.workspace_path = Path(workspace_path)
        self.config = config or CheckpointConfig()
        self._validate_workspace()
        self.last_commit_hash: Optional[str] = None

    @classmethod
    def create(
        cls,
        task_id: str,
        workspace_path: str,
        config: Optional[CheckpointConfig] = None,
    ) -> "CheckpointTracker":
        """
        Create and initialize a new checkpoint tracker.
        This is the preferred way to instantiate a tracker as it handles initialization.

        Args:
            task_id: Unique identifier for the task
            workspace_path: Path to the workspace to track
            config: Optional configuration settings

        Returns:
            Initialized CheckpointTracker instance

        Raises:
            WorkspaceError: If workspace validation fails
            GitError: If git initialization fails
        """
        tracker = cls(task_id, workspace_path, config)
        tracker.init_shadow_git()
        return tracker

    @classmethod
    def load(cls, task_id: str, storage_path: Optional[Path] = None) -> "CheckpointTracker":
        """
        Load an existing checkpoint tracker from storage.

        Args:
            task_id: The task ID of the checkpoint to load
            storage_path: Optional override for the storage location

        Returns:
            Loaded CheckpointTracker instance

        Raises:
            CheckpointNotFoundError: If no checkpoint exists for the task_id
            CheckpointError: If loading fails for other reasons
        """
        raise NotImplementedError

    def save_metadata(self) -> None:
        """
        Save checkpoint metadata to disk.
        This allows the checkpoint to be loaded later.

        Raises:
            CheckpointError: If saving fails
        """
        raise NotImplementedError

    def init_shadow_git(self) -> str:
        """
        Initialize the shadow git repository for tracking changes.

        Returns:
            Path to the initialized git repository

        Raises:
            GitError: If initialization fails
        """
        raise NotImplementedError

    def commit(self) -> Optional[str]:
        """
        Create a checkpoint of the current workspace state.

        Returns:
            Commit hash if successful, None otherwise

        Raises:
            GitError: If commit operation fails
        """
        raise NotImplementedError

    def reset_head(self, commit_hash: str) -> None:
        """
        Reset workspace to a specific checkpoint.

        Args:
            commit_hash: The commit hash to reset to

        Raises:
            GitError: If reset operation fails
        """
        raise NotImplementedError

    def get_diff_set(
        self, lhs_hash: Optional[str] = None, rhs_hash: Optional[str] = None
    ) -> List[DiffInfo]:
        """
        Get the differences between two checkpoints.

        Args:
            lhs_hash: Left-hand side commit hash (older)
            rhs_hash: Right-hand side commit hash (newer)

        Returns:
            List of file differences between the states

        Raises:
            GitError: If diff operation fails
        """
        raise NotImplementedError

    def _validate_workspace(self) -> None:
        """
        Validate the workspace path is acceptable for checkpointing.

        Raises:
            WorkspaceError: If workspace validation fails
        """
        raise NotImplementedError

    def cleanup(self) -> None:
        """
        Clean up resources used by the checkpoint tracker.
        Should be called when the tracker is no longer needed.
        """
        raise NotImplementedError

    def get_metadata(self) -> CheckpointMetadata:
        """
        Get metadata about the current checkpoint state.

        Returns:
            CheckpointMetadata object containing current state
        """
        return CheckpointMetadata(
            task_id=self.task_id,
            workspace_path=self.workspace_path,
            last_commit_hash=self.last_commit_hash,
            created_at=time.time(),
            config=self.config,
        )
