# =========================================================
# syncmodels
# =========================================================


class SyncModelException(Exception):
    "base for all SyncModel Exceptions"


class Recoverable(SyncModelException):
    """the request can be recovered."""


class NonRecoverable(SyncModelException):
    """the request can't be recovered.
    we need to advance the request.
    """


class BadData(SyncModelException):
    """Data is not properly formatted."""
