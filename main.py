import networkx as nx
import matplotlib.pyplot as plt
import random

class PostavkeGeneriranja:
    def __init__(self):
        self.brojRacunala = 10
        self.cvorovi = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        self.bridovi = [('f', 'd'), ('f', 'j'), ('f', 'c'), ('f', 'h'),
                        ('j', 'c'), ('j', 'b'), ('j', 'e'),
                        ('h', 'g'), ('h', 'd'),
                        ('d', 'g'), ('d', 'a'), ('d', 'c'),
                        ('c', 'e'), ('b', 'e'), ('a', 'b'), ('b', 'i'), ('e', 'i'), ('g', 'i'), ('c', 'a')]
        self.brojKontakataMin = 3
        self.brojKontakataMax = 5
        self.vrijemeSirenja = 1
        self.pocetakSirenja = 'a'
        self.krajSirenja = 'e'

    def dohvatiBrojRacunala(self):
        self.brojRacunala = int(input("Broj racunala = "))
        self.cvorovi = list(map(chr, range(97, 97+self.brojRacunala))) #riskirat ćemo i reći da nema više od 26 čvorova
        print(self.cvorovi)

    def dohvatiProsjecanBrojKontaka(self):
        brojKontakata = input("Broj kontakata (min - max) = ").split("-")
        self.brojKontakataMin = int(brojKontakata[0])
        self.brojKontakataMax = int(brojKontakata[1])

    def dohvatiVrijemeSirenja(self):
        self.vrijemeSirenja = int(input("Vrijeme potrebno za širenje zaraze = "))

    def dohvatiPocetakSirenja(self):
        self.pocetakSirenja = input("Pocetak sirenja (oznaka računala) = ")

    def dohvatiKrajSirenja(self):
        self.krajSirenja = input("Kraj sirenja (oznaka računala) = ")


postavke = PostavkeGeneriranja()


def dohvatiPostavke():
    postavke.dohvatiBrojRacunala()
    postavke.dohvatiProsjecanBrojKontaka()
    postavke.dohvatiVrijemeSirenja()
    postavke.dohvatiPocetakSirenja()
    postavke.dohvatiKrajSirenja()


def generirajBridove():
    postavke.bridovi = []
    for cvor in postavke.cvorovi:
        brojKontakata = random.randint(postavke.brojKontakataMin, postavke.brojKontakataMax)

        brojGeneriranihBridova = 0
        while brojGeneriranihBridova < brojKontakata:
            nasumicniKraj = random.randint(0, postavke.brojRacunala-1)

            if cvor == postavke.cvorovi[nasumicniKraj]:
                continue

            noviBrid = (cvor, postavke.cvorovi[nasumicniKraj])
            noviBridSuprotno = (postavke.cvorovi[nasumicniKraj], cvor)
            if noviBrid not in postavke.bridovi and noviBridSuprotno not in postavke.bridovi:
                postavke.bridovi.append(noviBrid)
            brojGeneriranihBridova += 1
    print(postavke.bridovi)

def izracunajNajkraciPut(G):
    cvorovi = nx.shortest_path(G, source=postavke.pocetakSirenja, target=postavke.krajSirenja, weight='weight')
    print(cvorovi)
    return cvorovi

def dohvatiOznaceneBridove(najkraciPut):
    bridovi = []
    for i in range(0, len(najkraciPut)-1):
        bridovi.append((najkraciPut[i], najkraciPut[i+1]))
        bridovi.append((najkraciPut[i+1], najkraciPut[i])) #isti brid, samo u obrnutom smjeru JUST IN CASE

    print(bridovi)
    return bridovi

def iscrtajGraf():
    G = nx.Graph()
    G.add_edges_from(postavke.bridovi, weight=postavke.vrijemeSirenja)

    values = [0.1 for node in G.nodes()]
    oznakeBridova = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    oznakeCvorova = {node: node for node in G.nodes()}

    crveniBridovi = dohvatiOznaceneBridove(izracunajNajkraciPut(G))
    bojeBridova = ['black' if not edge in crveniBridovi else 'red' for edge in G.edges()]

    pos = nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=oznakeBridova)
    nx.draw(G, pos, node_color=values, node_size=2000, edge_color=bojeBridova, edge_cmap=plt.cm.Reds)
    nx.draw_networkx_labels(G, pos, labels=oznakeCvorova)
    plt.show()

dohvatiPostavke()
generirajBridove()
iscrtajGraf()
