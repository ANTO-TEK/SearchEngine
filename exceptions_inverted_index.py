"""
Antonio Bove
mat. 0622701898
"""

class InvertedIndexException(Exception):

    def __init__(self, message = ""):
        super().__init__("Inverted Index Exception: " + message)

class OccurrenceListNotPresentException(InvertedIndexException):
    """Eccezione lanciata se la Occurrence List non è presente per la parola cercata"""

    def __init__(self, message = ""):
        super().__init__(message)
