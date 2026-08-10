"""Router and Handlers that must agree on param extraction."""


class Router:
    """Maps URL patterns to handlers and dispatches requests."""

    def __init__(self):
        self._routes = []

    def add_route(self, method, pattern, handler):
        """Register a route pattern with a handler.

        Pattern uses :param_name for dynamic segments.
        e.g., /users/:id/posts/:post_id
        """
        parts = [p for p in pattern.strip("/").split("/") if p]
        self._routes.append((method.upper(), parts, handler))

    def dispatch(self, method, path):
        """Match a path to a route and call the handler with extracted params.

        Returns the handler's result.
        Raises LookupError if no route matches.
        """
        path_parts = [p for p in path.strip("/").split("/") if p]
        method = method.upper()

        for route_method, route_parts, handler in self._routes:
            if route_method != method:
                continue
            if len(route_parts) != len(path_parts):
                continue
            params = {}
            match = True
            for route_seg, path_seg in zip(route_parts, path_parts):
                if route_seg.startswith(":"):
                    param_name = route_seg[1:]
                    params[param_name] = path_seg
                elif route_seg != path_seg:
                    match = False
                    break
            if match:
                return handler(params)

        raise LookupError(f"No route matches {method} {path}")


# --- Handlers ---
# Each handler receives a dict of params extracted by the router.

def get_user(params):
    """Handle GET /users/:id or /users/:user_id"""
    user_id = params.get("id") or params.get("user_id")
    return {"user_id": user_id, "action": "get_user"}


def list_users(params):
    """Handle GET /users (no params)"""
    return {"action": "list_users"}


def get_post(params):
    """Handle GET /users/:user_id/posts/:post_id"""
    result = dict(params)
    result["action"] = "get_post"
    return result


def create_user(params):
    """Handle POST /users"""
    return {"action": "create_user"}
