from typing import NamedTuple

class SubtitleSpeech(NamedTuple):
    """
    Representa uma fala da legenda com índice, timestamp e texto.
    """
    idx: int
    timestamp: str
    text: str
