import logging


class LoggingMixin:
    """Convenience super-class to have a logger configured with the class name"""

    _log: logging.Logger | None = None

    @property
    def log(self) -> logging.Logger:
        """Returns a logger."""
        if self._log is None:
            self._log = logging.getLogger(
                self.__class__.__module__ + "." + self.__class__.__name__
            )
        return self._log
