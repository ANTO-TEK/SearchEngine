"""
Antonio Bove
mat. 0622701898
"""

from exceptions_compressed_trie import *

class CompressedTrie:

    """Classe pubblica per la rappresentazione di un Compressed Trie"""

    #------------------------------------- nested _Node class -------------------------------------

    class _Node:

        """Classe privata per la memorizzazione di un nodo non foglia."""

        __slots__ = "_tag", "_parent", "_children"

        def __init__(self, tag, parent):
            """
            Costruttore della classe _Node.
            :param tag: etichetta del nodo
            :param parent: riferimento al padre del nodo
            Inoltre:
                -> children: riferimento a un dict che memorizza i figli di un nodo

            Complessità: O(1)
            """
            self._tag = tag
            self._parent = parent
            self._children = {}
    
    #------------------------------------- nested _WordNode class -------------------------------------

    class _WordNode(_Node):

        """Classe privata che estende la classe _Node per la memorizzazione di un nodo foglia. In particolare,
           viene aggiunto un riferimento a una lista di occorrenze.
        """
        
        __slots__ = "_occurrenceList"

        def __init__(self, tag, parent):
            """
            Costruttore della classe _WordNode
               
            Complessità: O(1)
            """
            super().__init__(tag, parent)
            self._occurrenceList = {}

    #--------------------------------- Initialize the CompressedTrie ---------------------------------

    __slots__ = '_root'

    def __init__(self):
        """
        Crea un Compressed Trie inizialmente vuoto

        Complessità: O(1)
        """
        self._root = self._Node(None, None)

    #------------------------------------- Public Interface -------------------------------------

    def insertWord(self, word):
        """
        Metodo pubblico che consente di inserire una nuova parola nel Compressed Trie.
        :param word: parola da inserire
        :return:

        Complessità: O(len(word)) expected
        """
        self._insertWordUtil(self._root, word + "$")

    def searchWord(self, word):
        """
        Metodo pubblico che consente la ricerca di una parola all'interno del Compressed Trie.
        :param word: parola da cercare
        :return: riferimento alla lista delle occorrenze della parola cercata

        Complessità: O(len(word)) expected
        """
        return self._searchWordUtil(self._root, word + "$")

    def printComressedTrieString(self):
        """
        Metodo pubblico che consente di visualizzare la struttura del Compressed Trie.
        :return:

        Complessità: O(n), con n uguale al numero di nodi del Trie
        """
        self._printComressedTrieStringUtil(self._root, 0)

    #-------------------------------------- Private Method --------------------------------------

    def _insertWordUtil(self, node, word):
        """
        Metodo privato di utilità che consente d'inserire una nuova parola nel Compressed Trie.

        :param node: nodo da cui partire per l'inserimento (nodo radice)
        :param word: parola da inserire
        :return:

        Complessità: O(len(word)) expected
        """
        # j indica in quale carattere della stringa originale mi trovo
        j = 0
        # salvo la lunghezza della parola iniziale
        sizeWord = len(word)
        while j < sizeWord:
            try:
                # controllo se il nodo corrente ha in children un nodo che ha un'etichetta che inizia con il carattere
                # iniziale della (sotto)stringa da inserire. Se presente, aggiorno node posizionandomi su di esso,
                # altrimenti viene lanciata un'eccezione
                node = node._children[word[j]]
                # a questo punto sono sicuro che il primo carattere della nuova etichetta del nodo corrisponda al primo
                # carattere della (sotto)stringa, e di conseguenza incremento j per controllare gli altri caratteri
                j += 1
                # si passa quindi a iterare sulla label del nodo corrente per verificare se questa corrisponde
                # completamente con la (sotto)stringa in esame
                if len(node._tag) > 1:
                    for i in range(1, len(node._tag)):
                        if word[j] != node._tag[i]:
                            # se si è verificato un mismatch, ho individuato il punto in cui effettuare una split e, a tal
                            # proposito effettuo una chiamata alla _nodeRestructure
                            self._nodeRestructure(node, node._tag, i)
                            # a questo punto, con la parte non comune della (sotto)stringa da inserire, creo un nuovo nodo foglia
                            # che sarà un figlio del nodo creato in fase di ristrutturazione
                            newLabel = word[j:]
                            newNode = self._WordNode(newLabel, node._parent)
                            node._parent._children[newLabel[0]] = newNode
                            return
                        # se si è verificato il match, vado avanti con il controllo
                        j += 1

            except KeyError:
                # in questo caso so che il nodo corrente non ha un nodo con un'etichetta che inizia come la (sotto)stringa
                # da inserire, pertanto posso creare un nuovo nodo foglia con l'intera (sotto)stringa
                node._children[word[j]] = self._WordNode(word[j:], node)
                return

    def _nodeRestructure(self, node, tag, counter): 
        """
        Metodo privato di utilità che si occupa della ristrutturazione di un nodo.

        :param node: nodo da ristrutturare
        :param tag: label del nodo da ristrutturare
        :param counter: lunghezza del prefisso comune
        :return:

        Complessità: O(1)
        """
        # padre del nodo da ristrutturare
        parent = node._parent
        # creo un nuovo nodo con la parte comune parte comune
        newNode = self._Node(tag[:counter], parent)
        # tra i figli del padre del nodo da ristrutturare, aggiorno il valore presente in corrispondenza della prima
        # lettera della parte comune con il nuovo nodo creato
        parent._children[newNode._tag[0]] = newNode
        # aggiorno la label del nodo da ristrutturare con la parte non comune del tag originale
        node._tag = tag[counter:]
        # aggiungo al nodo precedentemente creato il nodo appena modificato
        newNode._children[node._tag[0]] = node
        # assegno al nodo modificato il suo nuovo padre
        node._parent = newNode


    def _searchWordUtil(self, node, word):
        """

        Metodo privato di utilità che consente la ricerca di una parola nel Compressed Trie.

        :param node: nodo da cui partire per l'inserimento (nodo radice)
        :param word: parola da cercare
        :return:

        Complessità: O(len(word)) expected
        """
        # j indica in quale carattere della stringa originale mi trovo
        j = 0
        # salvo la lunghezza della parola iniziale
        sizeWord = len(word)
        while j < sizeWord:
            try:
                # controllo se il nodo corrente ha in children un nodo che ha un'etichetta che inizia con il carattere
                # iniziale della stringa da cercare. Se presente, aggiorno node posizionandomi su di esso,
                # altrimenti viene lanciata un'eccezione indicante che la parola non è presente
                node = node._children[word[j]]
                j += 1
                # si passa quindi a iterare sulla label del nodo corrente per verificare se questa corrisponde
                # completamente con la stringa in esame
                if len(node._tag) > 1:
                    for i in range(1, len(node._tag)):
                        if word[j] != node._tag[i]:
                            # se si è verificato un mismatch, viene lanciata un'eccezione indicante che la parola non è presente
                            raise WordNotPresentException("Parola non presente")
                        # se si è verificato il match, vado avanti con il controllo
                        j += 1
            except KeyError:
                raise WordNotPresentException("Parola non presente")
        # se sono giunto a questo punto, vuol dire che la parola è presente e restituisco la lista delle occorrenze associata
        if isinstance(node, self._WordNode):
            return node._occurrenceList

    def _printComressedTrieStringUtil(self, node, depth):
        """
        Metodo ricorsivo privato di utilità che consente di visualizzare la struttura del Compressed Trie.

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
            if isinstance(v, self._WordNode):
                print((depth * "---") + v._tag + " Occorrence List -> ", end='')
                for page, numOcc in v._occurrenceList.items():
                    print(str(numOcc) + " in pagina " + page.getUrl() + ", ", end='')
                print()
            else:
                print((depth * "---") + v._tag)
            self._printComressedTrieStringUtil(v, depth + 1)