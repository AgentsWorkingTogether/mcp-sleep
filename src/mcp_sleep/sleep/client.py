"""Base client module for Sleep interactions."""

import logging
from .config import SleepConfig

# Configure logging
logger = logging.getLogger("mcp-sleep")


class SleepClient:
    """Base client for Sleep interactions."""

    def __init__(self, config: SleepConfig | None = None) -> None:
        """Initialize the Sleep client with given or environment config.

        Args:
            config: Configuration for Sleep client. If None, will load from
                environment.

        Raises:
            ValueError: If configuration is invalid or environment variables
            are missing
        """
        self.config = config or SleepConfig.from_env()
