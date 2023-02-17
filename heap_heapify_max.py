"""
Antonio Bove
mat. 0622701898
"""

from TdP_collections.priority_queue.heap_priority_queue import HeapPriorityQueue

class _HeapHeapifyMax(HeapPriorityQueue):
    """Classe privata per la rappresentazione di un HeapHeapifyMax ottenuta estendendo la classe HeapPriorityQueue
       presente in TdP_collections, facendo l'override della classe _Item in modo da ottenere un heap maximum oriented
       e aggiungendo il metodo heapify per la costruzione dell'heap.

       La suddetta classe verrà utilizzata per effettuare il ranking delle pagine web nel metodo search della classe
       SearchEngine.
    """

    class _Item(HeapPriorityQueue._Item):
        """Classe privata innestata che estende la classe _Item presente nella classe HeapPriorityQueue"""

        def __init__(self, k, v):
            """
            Costruttore della classe _Item che inverte chiave e valore

            Complessità: O(1)
            """
            self._key = v
            self._value = k

        def __lt__(self, other):
            """
            Override del magic method __lt__ in modo da ottenere un heap maximum oriented.

            Complessità: O(1)
            """
            return self._key > other._key

    def __init__(self, contents=()):
        """
            Costruttore della classe HeapPriorityQueue.

            Di default, la coda sarà vuota. Se invece il contenuto è dato, questo dovrebbe essere una sequenza
            iterabile di coppie (k,v).

            Complessità: O(n + n) = O(2n) = O(n), con n uguale al numero di elementi nell'array
        """

        self._data = [self._Item(k, v) for k, v in contents.items()]
        if len(self._data) > 1:
            self._heapify()

    def _heapify(self):
        """
        Metodo privato per la costruzione dell'heap

        Complessità: O(n), con n uguale al numero di elementi nell'array di partenza
        """
        start = self._parent(len(self) - 1)  # inizia dal genitore dell'ultima foglia
        for j in range(start, -1, -1):  # scorre all'indietro fino alla radice
            self._downheap(j)
