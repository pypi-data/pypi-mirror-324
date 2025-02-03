from ..parsers import parse_bool


def test_parse_bool_true():
    for value in ['y', 'Y', 'yes', 'Yes', True, 'true', 'TRUE', 'True', 1, '1', 'on', 'ON', 'On']:
        assert parse_bool(value)


def test_parse_bool_false():
    for value in [0, False, 'False', 'false', 'FALSE', '0', 'no', 'NO', 'No', 'random_string']:
        assert not parse_bool(value)
