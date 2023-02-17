"""
Antonio Bove
mat. 0622701898
"""

from TdP_collections.map.avl_tree import AVLTreeMap

class Element:

    """Classe che rappresenta un elemento di un website. Può essere una pagina web o una directory"""

    #------------------------------- Initialize the Element -------------------------------

    __slots__ = '_name', '_isPage', '_content', '_website', '_url'

    def __init__(self, name, website, content=None):
        """
        Costruttore della classe Element.
        :param name: nome della pagina/directory
        :param website: riferimento al website a cui l'Element appartiene
        :param content:
            -> se content è None, l'Element è una directory e il suo contenuto è un oggetto
               AVLTreeMap che memorizza gli Element presenti nella directory
            -> altrimenti, l'Element è una pagina e il suo contenuto è una stringa che
               memorizza il contenuto della pagina
        In particolare:
           _isPage = False -> Element è una directory
           _isPage = True -> Element è una pagina
           _url -> riferimento alla risorsa web

        Complessità: O(1)
        """
        self._name = name
        self._website = website
        self._url = None

        if content is None:
            self._isPage = False
            self._content = AVLTreeMap()
        else:
            self._isPage = True
            self._content = content

    # ------------------------------- accessor methods - getters -------------------------------
    def getName(self):
        """
        Accessor method che restituisce l'attributo _name dell'oggetto Element
        :return: attributo _name

        Complessità: O(1)
        """
        return self._name

    def getPage(self):
        """
        Accessor method che restituisce l'attributo _isPage dell'oggetto Element
        :return: attributo _isPage

        Complessità: O(1)
        """
        return self._isPage

    def getContent(self):
        """
        Accessor method che restituisce l'attributo _content dell'oggetto Element
        :return: attributo _content

        Complessità: O(1)
        """
        return self._content

    def getWebsite(self):
        """
        Accessor method che restituisce l'attributo _website dell'oggetto Element
        :return: attributo _website

        Complessità: O(1)
        """
        return self._website

    def getUrl(self):
        """
        Accessor method che restituisce l'attributo _url dell'oggetto Element
        :return: attributo _url

        Complessità: O(1)
        """
        return self._url

    # ------------------------------- accessor methods - setters -------------------------------

    def setContent(self, content):
        """
        Accessor method che setta l'attributo _content dell'oggetto Element
        :param content: contenuto da inserire
        :return:

        Complessità: O(1)
        """
        self._content = content

    def setUrl(self, url):
        """
        Accessor method che setta l'attributo _url dell'oggetto Element
        :param url: url da inserire
        :return:

        Complessità: O(1)
        """
        self._url = url

    # ------------------------------- utility methods -------------------------------

    def isPage(self, page):
        """
        Metodo pubblico di utilità che consente di verificare se un oggetto Element è una pagina.
        :param page: oggetto Element da controllare
        :return: restituisce True se l'Element è una pagina, altrimenti False

        Complessità: O(1)
        """
        return page._isPage

    # ------------------------------- magic methods -------------------------------
    def __eq__(self, other):
        """
        Confronta due Element in base al loro url
        :param other: Element con cui confrontare
        :return: True se gli Element sono uguali, False altrimenti

        Complessità: O(1)
        """
        return type(other) is type(self) and self._url == other._url

    def __ne__(self, other):
        """
        Opposto di __eq__
        :param other: Element con cui confrontare
        :return: True se gli Element sono diversi, False altrimenti

        Complessità: O(1)
        """
        return not (self == other)

    def __lt__(self, other):
        """
        Confronta gli Element in base al loro url
        :param other: Element con cui confrontare
        :return: True se il primo Element è minore del secondo, False altrimenti

        Complessità: O(1)
        """
        return self._url < other._url

    def __hash__(self):
        """
        Magic method per il calcolo del valore hash di un oggetto Element in base al suo url
        :return: restituisce il valore hash calcolato

        Complessità: O(1)
        """
        return hash(self._url)
