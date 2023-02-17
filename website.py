"""
Antonio Bove
mat. 0622701898
"""

from element import Element
from exceptions_website import *

class WebSite:

    """Classe che rappresenta una raccolta di pagine Web che risiedono sullo stesso host"""

    #------------------------------- Initialize the Website -------------------------------

    __slots__ = '_homeDir', '_homepage'

    def __init__(self, host):
        """
        Costruttore della classe WebSite.
        :param host: nome della home directory

        Complessità: O(1)
        """
        # inizializzo la variabile _homeDir con un oggetto Element il cui nome è l'hostname e rappresenta una directory
        self._homeDir = Element(host, self)
        self._homepage = None

    #-------------------------------------- Private Method --------------------------------------

    def __isDir(self, elem):
        """
        Metodo privato che verifica se un oggetto Element è una directory.
        :param elem: oggetto Element
        :return: True se Element è una directory, altrimenti False

        Complessità: O(1)
        """
        return elem.getPage() is False

    def __isPage(self, elem):
        """
        Metodo privato che verifica se un oggetto Element è una pagina.
        :param elem: oggetto Element
        :return: True se Element è una pagina, altrimenti False

        Complessità: O(1)
        """
        return not self.__isDir(elem)

    def __hasDir(self, ndir, cdir):
        """
        Metodo privato che verifica se una directory è presente nella directory corrente.
        :param ndir: nome della directory da verificare
        :param cdir: oggetto Element che rappresenta la directory corrente
        :return: se cdir non è una directory o se ndir non è presente viene lanciata un'eccezione,
                 altrimenti viene restituito il riferimento all'oggetto Element che rappresenta la directory ndir

        Complessità: O(log k), dove k è il numero di elementi (file o directory) in cdir
        """
        if not self.__isDir(cdir):
            raise NotDirectoryException(cdir + " non è una directory")
        try:
            # verifico se cdir contiene un Element con nome ndir
            dir = cdir.getContent()[ndir.swapcase()]
            if not self.__isDir(dir):
                raise DirectoryNotExistsException("La directory " + ndir + " non esiste")
        except KeyError:
            raise DirectoryNotExistsException("La directory " + ndir + " non esiste")
        return dir

    def __newDir(self, ndir, cdir):
        """
        Metodo privato che verifica se una directory è presente nella directory corrente, altrimenti la crea.
        :param ndir: nome della directory da verificare
        :param cdir: oggetto Element che rappresenta la directory corrente
        :return: se ndir è presente viene restituito l'oggetto Element che rappresenta la directory ndir,
                 altrimenti viene creata in cdir tale cartella e restituito il riferimento all'oggetto
                 Element creato

        Complessità: O(log k), dove k è il numero di elementi (file o directory) in cdir
        """
        try:
            return self.__hasDir(ndir, cdir)
        except DirectoryNotExistsException:
            newDir = Element(ndir, self)
            cdir.getContent()[ndir.swapcase()] = newDir
            return newDir

    def __hasPage(self, npag, cdir):
        """
        Metodo privato che verifica se una pagina è presente nella directory corrente.
        :param npag: nome della pagina da verificare
        :param cdir: oggetto Element che rappresenta la directory corrente
        :return: se cdir non è una directory o se npag non è presente viene lanciata un'eccezione,
                 altrimenti viene restituito il riferimento all'oggetto Element che rappresenta la pagina npag

        Complessità: O(log k), dove k è il numero di elementi (file o directory) in cdir
        """
        if not self.__isDir(cdir):
            raise NotDirectoryException(cdir + " non è una directory")
        try:
            # verifico se cdir contiene un Element con nome npag
            page = cdir.getContent()[npag.swapcase()]
            if not self.__isPage(page):
                raise PageNotExistsException("La pagina " + npag + " non esiste")
        except KeyError:
            raise PageNotExistsException("La pagina " + npag + " non esiste")
        return page

    def __newPage(self, npag, cdir):
        """
        Metodo privato che verifica se una pagina è presente nella directory corrente, altrimenti la crea.
        :param npag: nome della pagina da verificare
        :param cdir: oggetto Element che rappresenta la directory corrente
        :return: se npag è presente viene restituito l'oggetto Element che rappresenta la pagina npag,
                 altrimenti viene creata in cdir tale pagina e restituito il riferimento all'oggetto
                 Element creato

        Complessità: O(log k), dove k è il numero di elementi (file o directory) in cdir
        """
        try:
            return self.__hasPage(npag, cdir)
        except PageNotExistsException:
            newPage = Element(npag, self, "")
            cdir.getContent()[npag.swapcase()] = newPage
            return newPage

    #------------------------------------- Public Interface -------------------------------------

    def getHomePage(self):
        """
        Metodo pubblico per ottenere la home page di un website
        :return: se la home page è presente restituisce l'oggetto Element a essa associato,
                 altrimenti lancia un'eccezione

        Complessità: O(1)
        """
        if self._homepage is None:
            raise HomepageNotExistsException("Homepage non esistente")
        return self._homepage

    def getSiteString(self):
        """
        Metodo pubblico che consente di ottenere una stringa che riflette la struttura del website
        :return: restituisce la stringa creata

        Complessità: O(n), dove n è il numero di pagine e directory del website
        """
        return self._inOrderTraversal(self._homeDir, "---", self._homeDir.getName() + "\n")

    def _inOrderTraversal(self, dir, dash, siteString):
        """
        Metodo privato ricorsivo che costruisce una stringa che riflette la struttura del website
        :param dir: directory corrente
        :param dash: moltiplicatore di dash
        :param siteString: stringa parziale
        :return: stringa che riflette la struttura del website

        Complessità: O(n), dove n è il numero di pagine e directory del website
        """
        # a partire dalla home directory visito tutte le directory e costruisco la stringa
        for item in dir.getContent().inorder():
            siteString += dash + " " + item.value().getName() + "\n"
            if self.__isDir(item.value()):
                # se l'item visitato è una directory chiamo ricorsivamente la funzione, incrementando il numero
                # di "---"
                siteString = self._inOrderTraversal(item.value(), dash + "---", siteString)
        return siteString

    def insertPage(self, url, content):
        """
        Metodo pubblico per l'inserimento di una nuova pagina nel website.
        :param url: stringa che rappresenta l'url della nuova pagina
        :param content: stringa che rappresenta il contenuto della nuova pagina
        :return: restituisce il riferimento alla pagina creata

        Complessità: O(l*log(k) + log(k)) < O(l*k), dove l è il numero di directory padre della pagina e
        k è il numero di pagine o directory contenute nell'ultima directory già esistente
        """
        # effettuo una split sull'url
        pathItems = url.split("/")
        # verifico che la pagina da inserire abbia come host lo stesso di quello del website, altrimenti viene lanciata
        # un'eccezione
        if not pathItems.pop(0) == self._homeDir.getName():
            raise HostInsertException("L'host dell'URL non coincide con quello del website in cui inserire la pagina")
        currDir = self._homeDir
        # salvo il numero di directory/file che costituiscono l'url
        size = len(pathItems)
        # itero sulla lista contenente le directory presenti nell'url fino al penultimo elemento che rappresenta il nome
        # della nuova pagina da inserire
        while len(pathItems) > 1:
            currDir = self.__newDir(pathItems.pop(0), currDir)
        # salvo il nome della pagina da inserire
        namePage = pathItems.pop(0)
        # creo la pagina nella directory corrente
        newPage = self.__newPage(namePage, currDir)
        # setto il contenuto della pagina e il suo url
        newPage.setContent(content)
        newPage.setUrl(url)
        # se l'url presenta, oltre al nome dell'host, solo la pagina 'index.html' vuol dire che questa è la homepage
        # del website e ne salvo il riferimento nell'oggetto Website
        if size == 1 and namePage == "index.html":
            self._homepage = newPage
        return newPage

    @staticmethod
    def getSiteFromPage(page):
        """
        Metodo pubblico statico che consente di ottenere il riferimento all'oggetto Website in cui una
        pagina è contenuta.
        :param page: oggetto Element rappresentante una pagina
        :return: se page è una pagina restituisce il riferimento all'oggetto website a cui essa appartiene,
                 altrimenti lancia un'eccezione

        Complessità: O(1)
        """
        if page.isPage(page):
            return page.getWebsite()
        raise NotPageException("L'elemento non è una pagina")

