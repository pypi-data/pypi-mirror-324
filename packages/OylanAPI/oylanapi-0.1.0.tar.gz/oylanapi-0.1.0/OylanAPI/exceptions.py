# exceptions.py

class OylanAPIError(Exception):
    """Base exception for Oylan API errors."""
    pass


class OylanAPIAuthError(OylanAPIError):
    """Authentication or authorization related errors."""
    pass


class OylanAPIRequestError(OylanAPIError):
    """Errors related to invalid requests (400)."""
    pass


class OylanAPINotFoundError(OylanAPIError):
    """Resource not found (404) errors."""
    pass


class OylanAPIServerError(OylanAPIError):
    """Server-side error (5xx) from Oylan API."""
    pass
