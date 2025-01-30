import pytest

from milgeo.color import ColorFinder


@pytest.fixture
def color_finder():
    color_finder = ColorFinder()
    return color_finder


def test_hex_color(color_finder):
    assert color_finder.find_hex_color("Here is a color: #ff5733") == "#ff5733"
    assert color_finder.find_hex_color("<color>#ff888888</color>") == "#888888"
    assert color_finder.find_hex_color("<color>#ff00ffff</color>") == "#00ffff"
    assert color_finder.find_hex_color("The sky is dodgerblue") == "#0000ff"
    assert color_finder.find_hex_color("rgb(255, 99, 71)") == "#ff6347"


def test_rgb_color(color_finder):
    assert color_finder.find_hex_color("Here is a color: rgb(255, 87, 51)") == "#ff5733"


def test_named_color(color_finder):
    assert color_finder.find_hex_color("Here is a color: bLueasdsad") == "#0000ff"


def test_no_color(color_finder):
    assert color_finder.find_hex_color("There are no colors here.") is None


def test_mixed_colors(color_finder):
    assert color_finder.find_hex_color("Color in hex: #123456 and rgb: rgb(18, 52, 86)") == "#123456"


@pytest.mark.parametrize("hex_color, opacity, expected_output", [
    ("#ff5733", 1.0, "ffff5733"),
    ("#ff5733", 0.5, "7fff5733"),
    ("#ff5733", 0.0, "00ff5733"),
    ("ff5733", 1.0, "ffff5733"),
    ("ff5733", 0.5, "7fff5733"),
    ("ff5733", 0.0, "00ff5733"),
    ("#ffff5733", 1.0, "ffff5733"),
    ("#ffff5733", 0.5, "7fff5733"),
    ("#ffff5733", 0.0, "00ff5733"),
])
def test_make_argb_color(hex_color, opacity, expected_output):
    assert ColorFinder.make_argb_color(hex_color, opacity) == expected_output
