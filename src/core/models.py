from typing import NamedTuple

class SubtitleBlock(NamedTuple):
    """
    Representa um bloco de legenda com índice, timestamp e texto.
    """
    idx: int
    timestamp: str
    text: str
