# Router & Handler System

## Problem

Implement a URL routing system with two parts that must agree on how URL parameters are extracted and passed:

1. **`Router`** - Matches URL patterns and dispatches to handlers:
   - `add_route(method, pattern, handler)` - Registers a URL pattern (e.g., `"/users/:id"`) with a handler function.
   - `dispatch(method, path)` - Matches the given path against registered patterns, extracts parameters, and calls the matched handler with those params. Raises `LookupError` if no match.

2. **Handler functions** - Receive extracted parameters and return results:
   - `get_user(params)` - Returns `{"user_id": <id>, "action": "get_user"}`
   - `list_users(params)` - Returns `{"action": "list_users"}`
   - `get_post(params)` - Returns all params plus `{"action": "get_post"}`
   - `create_user(params)` - Returns `{"action": "create_user"}`

## URL Pattern Syntax

- Static segments match literally: `/users` matches only `/users`
- Dynamic segments start with `:`: `/users/:id` matches `/users/42` and extracts `{"id": "42"}`
- Multiple params: `/users/:user_id/posts/:post_id` extracts both

## Interface Contract

- Router calls `handler(params)` where `params` is a dict of `{param_name: value}`.
- Param values are always strings.
- Method matching is case-insensitive (GET == get).
- Trailing slashes should be normalized (ignored).
- Handlers receive exactly the params defined in the pattern—no more, no less.

## Constraints

- Do NOT use any external routing library.
- Both Router and all handler functions must be in the same `solution.py` file.
