"""Router and Handler system.

URL patterns use :param_name for dynamic segments.
Handlers receive a dict of extracted params.
"""


class Router:
    """Maps URL patterns to handlers and dispatches requests."""

    def __init__(self):
        raise NotImplementedError

    def add_route(self, method, pattern, handler):
        """Register a route. Pattern uses :name for dynamic segments."""
        raise NotImplementedError

    def dispatch(self, method, path):
        """Match path, extract params, call handler. Raises LookupError if no match."""
        raise NotImplementedError


def get_user(params):
    """Handle GET /users/:id - return {"user_id": <id>, "action": "get_user"}"""
    raise NotImplementedError


def list_users(params):
    """Handle GET /users - return {"action": "list_users"}"""
    raise NotImplementedError


def get_post(params):
    """Handle GET /users/:user_id/posts/:post_id - return all params + action"""
    raise NotImplementedError


def create_user(params):
    """Handle POST /users - return {"action": "create_user"}"""
    raise NotImplementedError
