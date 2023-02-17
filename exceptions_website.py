"""
Antonio Bove
mat. 0622701898
"""

class WebsiteException(Exception):

    def __init__(self, message = ""):
        super().__init__("Website Exception: " + message)

class HomepageNotExistsException(WebsiteException):
    """Eccezione lanciata quando la homepage non è presente"""

    def __init__(self, message = ""):
        super().__init__(message)

class NotDirectoryException(WebsiteException):
    """Eccezione lanciata se l'Element non è una directory"""

    def __init__(self, message = ""):
        super().__init__(message)

class NotPageException(WebsiteException):
    """Eccezione lanciata se l'Element non è una pagina"""

    def __init__(self, message = ""):
        super().__init__(message)

class DirectoryNotExistsException(WebsiteException):
    """Eccezione lanciata se la directory non esiste"""

    def __init__(self, message = ""):
        super().__init__(message)


class PageNotExistsException(WebsiteException):
    """Eccezione lanciata se la pagina non esiste"""

    def __init__(self, message = ""):
        super().__init__(message)


class HostInsertException(WebsiteException):
    """Eccezione lanciata se l'host dell'URL non coincide con quello del website in cui inserire la pagina"""

    def __init__(self, message = ""):
        super().__init__(message)
