import pytest

from friendly_names import generate


def test_default_generation():
    """Test default name generation"""
    name = generate()
    parts = name.split("-")
    assert len(parts) == 3
    assert "-" in name


def test_custom_word_count():
    """Test generating names with different word counts"""
    name = generate(words=2)
    assert len(name.split("-")) == 2

    name = generate(words=4)
    assert len(name.split("-")) == 4


def test_custom_separator():
    """Test using different separators"""
    name = generate(separator="_")
    assert "_" in name
    assert "-" not in name


def test_invalid_word_count():
    """Test that invalid word counts raise ValueError"""
    with pytest.raises(ValueError):
        generate(words=0)
