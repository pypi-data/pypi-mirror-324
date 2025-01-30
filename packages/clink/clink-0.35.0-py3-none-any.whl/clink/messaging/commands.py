import logging

from . import base


__all__ = ["Command"]


logger = logging.getLogger(__name__)


class BaseCommand(base.BaseMessage):
    """Base command."""

    pass


class Command(BaseCommand):
    """Command."""

    pass
