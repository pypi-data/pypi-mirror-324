from pathlib import Path
from typing import List

import tiktoken
from ascii_colors import ASCIIColors
from datetime import datetime

class Tokenizer:
    def __init__(self, name):
        ASCIIColors.multicolor(
            [f"[LollmsVectorDB][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]", f" Using tokenizer {name}"],
            [ASCIIColors.color_red, ASCIIColors.color_cyan],
        )

    def tokenize(self, text: str) -> List[int]:
        """
        Tokenizes the input text into a list of tokens.

        Args:
            text (str): The text to tokenize.

        Returns:
            List[int]: A list of tokens.
        """
        raise NotImplementedError(
            "Tokenize method not implemented. It's like trying to drive a car without wheels!"
        )

    def detokenize(self, tokens: List[int]) -> str:
        """
        Detokenizes a list of tokens back into text.

        Args:
            tokens (List[int]): The list of tokens to detokenize.

        Returns:
            str: The detokenized text.
        """
        raise NotImplementedError(
            "Detokenize method not implemented. It's like trying to bake a cake without an oven!"
        )
