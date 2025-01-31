"""
Python Checkpoint System
A Git-based workspace state management system.
"""

from .interface import (
    CheckpointConfig,
    CheckpointError,
    CheckpointTracker,
    DiffInfo,
    GitError,
    RestoreType,
    WorkspaceError,
)

__version__ = "0.1.0"
__all__ = [
    "CheckpointError",
    "WorkspaceError",
    "GitError",
    "DiffInfo",
    "RestoreType",
    "CheckpointConfig",
    "CheckpointTracker",
]
