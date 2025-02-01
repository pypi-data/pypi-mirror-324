# SPDX-FileCopyrightText: 2025-present James Kassemi <james@kassemi.org>
#
# SPDX-License-Identifier: MIT

import random

from .adjectives import ADJECTIVES
from .nouns import NOUNS
from .verbs import VERBS


def generate(words: int = 3, separator: str = "-") -> str:
    """
    Generate a friendly random name.

    Args:
        words: Number of words to include in the name (default: 3)
        separator: String to use between words (default: "-")

    Returns:
        A friendly name string like "red-loop-bounty"

    Examples:
        >>> generate()
        'swift-running-river'
        >>> generate(words=2)
        'blue-mountain'
        >>> generate(separator="_")
        'happy_dancing_star'
    """
    if words < 1:
        raise ValueError("words must be at least 1")

    name_parts = []

    # First word is always an adjective
    name_parts.append(random.choice(ADJECTIVES))

    # Middle words (if any) are verbs
    for _ in range(max(0, words - 2)):
        name_parts.append(random.choice(VERBS))

    # Last word is always a noun
    if words > 1:
        name_parts.append(random.choice(NOUNS))

    return separator.join(name_parts)
