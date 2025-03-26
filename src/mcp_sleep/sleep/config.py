"""Configuration module for the Sleep."""

import os
from dataclasses import dataclass


@dataclass
class SleepConfig:
    """Sleep configuration."""
    timeout: int  # Max wait timeout

    @classmethod
    def from_env(cls) -> "SleepConfig":
        """Create configuration from environment variables.

        Returns:
            SleepConfig with values from environment variables

        Raises:
            ValueError: If any required environment variable is missing
        """
        timeout = int(os.getenv("MCP_SLEEP_TIMEOUT"))

        return cls(
            timeout=timeout
        )
