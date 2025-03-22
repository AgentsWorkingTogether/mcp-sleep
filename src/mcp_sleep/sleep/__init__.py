# flake8: noqa: E501
"""Sleep integration module.

This module provides access to Sleep through the Model Context
Protocol.
"""

from .wait import WaitMixin
from .client import SleepClient
from .config import SleepConfig

class SleepFetcher(WaitMixin):
    """Main entry point for Sleep operations, providing backward
    compatibility.

    This class combines functionality from various mixins to maintain the same
    API as the original SleepFetcher class.
    """

    pass

__all__ = ["SleepFetcher","SleepConfig", "SleepClient"]
