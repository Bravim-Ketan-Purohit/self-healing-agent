import pytest
from solution import Router, get_user, list_users, get_post, create_user


def test_multiple_params():
    router = Router()
    router.add_route("GET", "/users/:user_id/posts/:post_id", get_post)
    result = router.dispatch("GET", "/users/42/posts/7")
    assert result == {"user_id": "42", "post_id": "7", "action": "get_post"}


def test_no_params_route():
    router = Router()
    router.add_route("GET", "/users", list_users)
    result = router.dispatch("GET", "/users")
    assert result == {"action": "list_users"}


def test_method_not_found():
    router = Router()
    router.add_route("GET", "/users/:id", get_user)
    with pytest.raises(LookupError):
        router.dispatch("POST", "/users/1")


def test_path_not_found():
    router = Router()
    router.add_route("GET", "/users/:id", get_user)
    with pytest.raises(LookupError):
        router.dispatch("GET", "/unknown/path")


def test_trailing_slash_normalized():
    router = Router()
    router.add_route("GET", "/users/:id", get_user)
    result = router.dispatch("GET", "/users/5/")
    assert result == {"user_id": "5", "action": "get_user"}


def test_post_method_with_handler():
    router = Router()
    router.add_route("POST", "/users", create_user)
    result = router.dispatch("POST", "/users")
    assert result == {"action": "create_user"}


def test_same_pattern_different_methods():
    router = Router()
    router.add_route("GET", "/users/:id", get_user)
    router.add_route("POST", "/users", create_user)
    assert router.dispatch("GET", "/users/99") == {"user_id": "99", "action": "get_user"}
    assert router.dispatch("POST", "/users") == {"action": "create_user"}


def test_long_path():
    router = Router()
    router.add_route("GET", "/api/v1/users/:id/posts/:pid/comments/:cid", get_post)
    result = router.dispatch("GET", "/api/v1/users/1/posts/2/comments/3")
    assert result == {"id": "1", "pid": "2", "cid": "3", "action": "get_post"}
