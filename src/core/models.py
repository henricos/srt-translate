from typing import NamedTuple

class SubtitleBlock(NamedTuple):
    """
    Representa um bloco de legenda com índice, timestamp e texto.
    """
    index: int
    timestamp: str
    text: str
