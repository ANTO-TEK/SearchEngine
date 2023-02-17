"""
Antonio Bove
mat. 0622701898
"""

class CompressedTrieException(Exception):

    def __init__(self, message = ""):
        super().__init__("Compressed Trie Exception: " + message)

class WordNotPresentException(CompressedTrieException):
    """Eccezione lanciata quando cerchiamo una parola non presente"""

    def __init__(self, message = ""):
        super().__init__(message)
