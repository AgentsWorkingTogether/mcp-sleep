"""Module for Sleep waits operations."""

import asyncio
import logging

from .client import SleepClient

logger = logging.getLogger("mcp-sleep")


class WaitMixin(SleepClient):
    """Mixin for Sleep waits operations."""

    async def wait(self, seconds) -> None:
        """
        Get an aggregated overview of findings and resources grouped by providers.

        Returns:
            Dictionary containing provider information with results and
            metadata
        """  # noqa: E501
        await asyncio.sleep(seconds)
        return
