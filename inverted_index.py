"""
Antonio Bove
mat. 0622701898
"""

from compressed_trie import CompressedTrie
from element import Element
from exceptions_inverted_index import *

class InvertedIndex:
    """Classe pubblica per la rappresentazione di un Inverted Index"""

    __slots__ = '_compressedTrie'

    def __init__(self):
        """
        Costruttore della classe InvertedIndex.
        Crea un InvertedIndex vuoto istanziando un oggetto CompressedTrie.

        Complessità: O(1)
        """
        self._compressedTrie = CompressedTrie()

    def addWord(self, keyword):
        """
        Metodo pubblico che consente di aggiungere la parola keyword all'InvertedIndex

        :param keyword: parola da aggiungere
        :return:

        Complessità: O(len(keyword)) expected
        """
        self._compressedTrie.insertWord(keyword)

    def addPage(self, page):
        """
        Metodo pubblico che consente di elaborare l'Element page, e per ogni parola nel suo contenuto,
        questa viene inserita nell'InvertedIndex se non è presente, e la pagina viene inserita nella
        lista delle occorrenze di questa parola. La lista delle occorrenze memorizza anche il numero di
        occorrenze della parola nella pagina.
        In particolare, dal momento in cui la lista delle occorrenze è rappresentata da una ProbeHashMap,
        viene utilizzata come chiave la pagina e come valore il numero di occorrenze della parola in quella
        pagina.

        :param page: Element page da processare
        :return:

        Complessità: O(len(word)) + O(len(word)) + O(1) amortized ed expected < O(len(word) + log(list(word)) amortized
                     ed expected, per ogni parola nel contenuto della pagina, con list(word) pari al numero di pagine
                     nella lista delle occorrenze della parola.
        """
        if not isinstance(page, Element): raise TypeError("L'argomento non è un Element")
        if not page.getPage(): raise TypeError("L'argomento non è una pagina")
        words = page.getContent().split()
        for word in words:
            self.addWord(word)
            occList = self.getList(word)
            try:
                occList[page] += 1
            except KeyError:
                occList[page] = 1

    def getList(self, keyword):
        """
        Metodo pubblico che consente di ottenere il riferimento alla lista delle occorrenze di una
        specifica parola.

        :param keyword: parola di cui si vuole conoscere la lista delle occorrenze
        :return: restituisce la corrispondente lista delle occorrenzd se presente, altrimenti lancia una
                 eccezione

        Complessità: O(len(keyword)) expected
        """
        try:
            return self._compressedTrie.searchWord(keyword)
        except:
            raise OccurrenceListNotPresentException("Occurrence List non presente per la parola " + keyword)
