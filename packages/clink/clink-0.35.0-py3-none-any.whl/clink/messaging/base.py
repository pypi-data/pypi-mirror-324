import logging
from dataclasses import dataclass


__all__: list = []


logger = logging.getLogger(__name__)


@dataclass
class BaseMessage:
    """Base message."""

    pass
