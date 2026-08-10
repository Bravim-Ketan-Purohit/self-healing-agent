import pytest
from solution import Router, get_user, list_users, get_post


def test_basic_param_extraction():
    router = Router()
    router.add_route("GET", "/users/:id", get_user)
    result = router.dispatch("GET", "/users/42")
    assert result == {"user_id": "42", "action": "get_user"}


def test_static_route():
    router = Router()
    router.add_route("GET", "/users", list_users)
    result = router.dispatch("GET", "/users")
    assert result == {"action": "list_users"}


def test_multi_param():
    router = Router()
    router.add_route("GET", "/users/:user_id/posts/:post_id", get_post)
    result = router.dispatch("GET", "/users/1/posts/99")
    assert result == {"user_id": "1", "post_id": "99", "action": "get_post"}


def test_no_match_raises():
    router = Router()
    router.add_route("GET", "/users/:id", get_user)
    with pytest.raises(LookupError):
        router.dispatch("GET", "/posts/1")
