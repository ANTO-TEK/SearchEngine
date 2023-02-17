"""
Antonio Bove
mat. 0622701898
"""

"""
    CLASSE NON UTILIZZATA NEL PROGETTO, REALIZZATA SOLO PER TEST
"""

from exceptions_standard_trie import *

class StandardTrie:

    """Classe pubblica per la rappresentazione di uno Standard Trie"""

    #------------------------------------- nested _Node class -------------------------------------

    class _Node:

        """Classe privata per la memorizzazione di un nodo."""

        __slots__ = "_children", "_endOfNode", "_occurrenceList"

        def __init__(self):
            """
            Costruttore della classe _Node.

                • children: riferimento a un dict che memorizza i figli di un nodo
                • endOfNode: True se il nodo rappresenta la fine di una parola, False altrimenti
                • occurrenceList: riferimento a una ProbeHashMap che memorizza, per ogni nodo che rappresenta la fine
                                  di una parola, la lista delle occorrenze

            Complessità: O(1)
            """
            self._endOfNode = False
            self._children = {}

    #------------------------------- Initialize the StandardTrie -------------------------------

    __slots__ = '_root'

    def __init__(self):
        """
        Creo un Standard Trie inizialmente vuoto

        Complessità: O(1)
        """
        self._root = self._Node()

    #------------------------------------- Public Interface -------------------------------------

    def insertWord(self, word):
        """
        Metodo pubblico che consente d'inserire una nuova parola nello Standard Trie.
        :param word: parola da inserire
        :return:

        Complessità: O(len(word)) expected
        """
        self._insertWordUtil(self._root, word)

    def searchWord(self, word):
        """
        Metodo pubblico che consente la ricerca di una parola all'interno dello Standard Trie.
        :param word: parola da cercare
        :return: riferimento alla lista delle occorrenze della parola cercata

        Complessità: O(len(word)) expected
        """
        return self._searchWordUtil(self._root, word)

    def printComressedTrieString(self):
        """
        Metodo pubblico che consente di visualizzare la struttura dello Standard Trie.
        :return:

        Complessità: O(n), con n uguale al numero di nodi del Trie
        """
        self._printComressedTrieStringUtil(self._root, 0)

    #-------------------------------------- Private Method --------------------------------------

    def _insertWordUtil(self, node, word):
        """
        Metodo privato di utilità che consente d'inserire una nuova parola nello Standard Trie.

        :param node: nodo da cui partire per l'inserimento (nodo radice)
        :param word: parola da inserire
        :return:

        Complessità: O(len(word)) expected
        """
        # salvo la dimensione della parola da inserire
        size = len(word)
        # itero sulla lunghezza della parola
        for i in range(size):
            try:
                # verifico se l'i-esima lettera della parola è presente tra i figli del nodo corrente
                node = node._children[word[i]]
            except KeyError:
                # nel caso in cui non fosse presente, itero sulla porzione di parola non presente e creo i nuovi nodi
                for j in range(i, size):
                    newNode = self._Node()
                    node._children[word[j]] = newNode
                    node = newNode
                # marchio l'ultimo nodo come terminatore per la parola inserita, gli associo una lista delle occorrenze
                # ed esco dalla funzione
                node._endOfNode = True
                node._occurrenceList = {}
                return
        # se siamo arrivati a questo punto vuol dire che nel Trie è presente un prefisso che corrisponde proprio alla
        # parola da inserire. Pertanto, controllo che la parola non sia stata già inserita in precedenza, e in tal caso
        # marchio il nodo corrente come un end node e gli associo una lista delle occorrenze
        if not node._endOfNode:
            node._endOfNode = True
            node._occurrenceList = {}

    def _searchWordUtil(self, node, word):
        """

        Metodo privato di utilità che consente la ricerca di una parola nello Standard Trie.

        :param node: nodo da cui partire per l'inserimento (nodo radice)
        :param word: parola da cercare
        :return:

        Complessità: O(len(word)) expected
        """
        # itero sulla lunghezza della parola
        for i in range(len(word)):
            try:
                # verifico se l'i-esima lettera della parola è presente tra i figli del nodo corrente
                node = node._children[word[i]]
            except KeyError:
                # se si verifica un mismatch, vuol dire che la parola non è presente e lancio un'eccezione
                raise WordNotPresentException("Parola non presente")
        # se sono arrivato a questo punto vuol dire che nel Trie è presente sicuramente un prefisso della parola
        # che sto cercando. Pertanto, mi assicuro che l'ultimo nodo sia un end node prima di restituire la lista
        # delle occorrenze
        if node._endOfNode:
            return node._occurrenceList
        raise WordNotPresentException("Parola non presente")

    def _printComressedTrieStringUtil(self, node, depth):
        """
        Metodo ricorsivo privato di utilità che consente di visualizzare la struttura dello Standard Trie.

        :param node: nodo da cui partire (radice)
        :param depth: profondità
        :return:

        Complessità: O(n), con n uguale al numero di nodi del Trie
        """
        # se il Trie è vuoto esco dalla funzione
        if len(node._children) == 0:
            return
        # itero sui figli di ciascun nodo
        for k, v in node._children.items():
            # se il nodo è una foglia stampo anche la lista delle occorrenze associata
            if v._endOfNode:
                print((depth * "---") + k + " Occorrence List -> ", end='')
                for page, numOcc in v._occurrenceList.items():
                    print(str(numOcc) + " in pagina " + page.getUrl() + ", ", end='')
                print()
            else:
                print((depth * "---") + k)
            self._printComressedTrieStringUtil(v, depth + 1)