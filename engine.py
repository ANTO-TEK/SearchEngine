"""
Antonio Bove
mat. 0622701898
"""

import os
from TdP_collections.hash_table.probe_hash_map import ProbeHashMap
from website import WebSite
from inverted_index import InvertedIndex
from heap_heapify_max import _HeapHeapifyMax

class SearchEngine:
    """Classe pubblica per la rappresentazione di un SearchEngine"""

    __slots__ = '_websites', '_invertedIndex'

    def __init__(self, namedir):
        """
        Costruttore della classe che inizializza il SearchEngine, prendendo in input una directory in cui sono
        presenti più file, ognuno dei quali rappresenta una pagina web diversa.
        Ogni file contiene nella prima riga l'URL (compreso l'hostname) e nelle righe successive il contenuto della
        pagina web. Questa funzione popola il database del motore di ricerca, inizializzando e inserendo valori in tutte
        le strutture dati necessarie.

        :param namedir: directory di input
        """
        self._websites = ProbeHashMap()
        self._invertedIndex = InvertedIndex()
        currPath = os.getcwd()  # ottengo il path della directory di lavoro corrente
        os.chdir(namedir)  # mi sposto nella cartella in cui sono contenuti i file

        for file in os.listdir():  # itero su tutti i file
            if file.endswith(".txt"):  # controllo che il file sia un file di testo
                self._updateStructures(file)
        os.chdir(currPath)  # ritorno alla cartella di lavoro precedente

    def _updateStructures(self, file):
        """
        Metodo privato di utilità che consente, dopo aver invocato il metodo per la lettura del file, d'inserire
        nell'apposita struttura dati il website se non presente, aggiunge la pagina al website e all'InvertedIndex.

        :param file: nome del file da leggere
        :return:
        """
        url, content = self._readFile(file)
        host = url.split("/")[0]
        try:
            site = self._websites[host]
        except KeyError:
            site = WebSite(host)
            self._websites[host] = site
        newPage = site.insertPage(url[:-1], content)
        self._invertedIndex.addPage(newPage)

    def _readFile(self, file):
        """
        Metodo privato di utilità che si occupa di aprile il leggere, leggerne il contenuto e chiuderlo.

        :param file: nome del file da leggere
        :return: restituisce la prima linea del file che corrisponde all'URL e il contenuto effettivo della pagina
                 web.
        """
        with open(file, 'r') as f:
            return f.readline(), f.read()


    def search(self, keyword, k):
        """
        Metodo pubblico che consente di cercare le k pagine web con il numero massimo di occorrenze della parola chiave
        ricercata.

        :param keyword: parola da cercare
        :param k: pagine web con il numero massimo di occorrenze della parola keyword
        :return: restituisce una stringa s costruita come segue: per ciascuna di queste k pagine ordinate in ordine
                 decrescente di occorrenze, a s vengono aggiunte le stringhe del sito che ospita quella pagina, a meno
                 che questo sito non sia già stato inserito.
        """
        # attraverso il metodo getList ottengo il riferimento alla lista delle occorrenze associata alla keyword
        occList = self._invertedIndex.getList(keyword)
        # creo un heap maximum oriented a partire dalla lista delle occorrenze (RedBlackTreeMap) passandolo come
        # parametro al costruttore, ordinato in base al numero di occorrenze (utilizzando quindi come chiave il
        # numero di occorrenze e come valore la pagina)
        heapMax = _HeapHeapifyMax(occList)
        # creo una hash table di supporto per gestire il fatto che un sito può essere presente più volte
        tmpDict = ProbeHashMap()
        # inizializzo una stringa vuota che dovrà contenere l'esito della ricerca
        s = ""

        # calcolo il minimo tra k (numero pagine web con il numero massimo di occorrenze della parola chiave ricercata)
        # e la lunghezza della lista delle occorrenze. Questo perché se ad esempio k = 5 e len(occList) = 10 sicuramente
        # non estrarremo più di k elementi dall'heap e viceversa, se k = 10 e len(occList) = 5 sicuramente non
        # potremmo fare più di len(occList) estrazioni dall'heap
        numMin = min(k, len(occList))
        for i in range(numMin):
            # estraggo il massimo dall'heap (essendo maximum oriented la remove_min restituirà il massimo)
            elem = heapMax.remove_min()
            try:
                # ottengo l'hostname dall'url della pagina
                hostname = elem[1].getUrl().split("/")[0]
                # se l'hostname è già presente nella struttura di appoggio non viene eseguita nessuna operazione perché
                # vuol dire che è già stato considerato nella costruzione della stringa
                tmpDict[hostname]
            except KeyError:
                # se l'hostname non è presente lo aggiungo e concateno alla stringa finale la struttura del website a
                # cui la pagina appartiene
                tmpDict[hostname] = True
                s += WebSite.getSiteFromPage(elem[1]).getSiteString()
        return s[:-1]




