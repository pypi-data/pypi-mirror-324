from src.piscada_foresight import http_piscada


def test_get_state_file():
    state_file = http_piscada._get_state_file("test")
    assert str(state_file).endswith("/.test_state")
    assert str(state_file).startswith("/")
