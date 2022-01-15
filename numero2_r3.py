import networkx as nx
import matplotlib.pyplot as plt
import random

class PostavkeGeneriranja:
    def __init__(self):
        self.brojRacunala = 10
        self.cvorovi = ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']
        self.bridovi = [('b1', 'c1'), ('b1', 'c2'), ('b1', 'b2'), ('b2', 'c2'), ('b2', 'c1'),
                        ('c1', 'c2'), ('c1', 'a2'), ('c1', 'a1'), ('c1', 'c2'), ('c2', 'a2')]
        self.pocetakSirenja = 'b1'
        self.krajSirenja = 'a2'
        self.kategorije = {'a': (5, 6), 'b': (3, 4), 'c': (1, 2)}
        self.dozvoljeniBridovi = {'aa', 'bb', 'cc', 'ab', 'ac', 'bc'}
        self.tezine = {'aa': 2, 'bb': 4, 'cc': 6, 'ab': 3, 'ac': 4, 'bc': 5}
        self.brojeviPoKat = {}

    def dohvatiBrojRacunala(self):
        self.brojRacunala = int(input("Broj racunala = "))
        self.cvorovi = list(map(chr, range(97, 97+self.brojRacunala)))

    def dohvatiPocetakSirenja(self):
        self.pocetakSirenja = input("Pocetak sirenja (oznaka računala) = ")

    def dohvatiKrajSirenja(self):
        self.krajSirenja = input("Kraj sirenja (oznaka računala) = ")

postavke = PostavkeGeneriranja()

def dohvatiPostavke():
    postavke.dohvatiBrojRacunala()

def dohvatiOstatakPostavki():
    postavke.dohvatiPocetakSirenja()
    postavke.dohvatiKrajSirenja()

def generirajBridove():
    postavke.bridovi = []
    for cvor in postavke.cvorovi:
        oznakaCvora = cvor[0]
        kategorija = postavke.kategorije[oznakaCvora]
        brojKontakata = random.randint(kategorija[0], kategorija[1])

        brojGeneriranihBridova = 0
        while brojGeneriranihBridova < brojKontakata:
            nasumicniKraj = random.randint(0, postavke.brojRacunala-1)

            if cvor == postavke.cvorovi[nasumicniKraj]:
                continue

            oznakaBrida = oznakaCvora + postavke.cvorovi[nasumicniKraj][0]
            oznakaBridaSuprotno = postavke.cvorovi[nasumicniKraj][0] + oznakaCvora
            if oznakaBrida not in postavke.dozvoljeniBridovi and oznakaBridaSuprotno not in postavke.dozvoljeniBridovi:
                continue

            noviBrid = (cvor, postavke.cvorovi[nasumicniKraj])
            noviBridSuprotno = (postavke.cvorovi[nasumicniKraj], cvor)
            if noviBrid not in postavke.bridovi and noviBridSuprotno not in postavke.bridovi:
                postavke.bridovi.append(noviBrid)
            brojGeneriranihBridova += 1

def dohvatiTezinuBrida(brid):
    oznakeBrida = brid[0][0] + brid[1][0]
    oznakeBridaObrnuto = brid[1][0] + brid[0][0]

    tezina = 0
    if oznakeBrida not in postavke.tezine:
        tezina = postavke.tezine[oznakeBridaObrnuto]
    else:
        tezina = postavke.tezine[oznakeBrida]

    return tezina

def generirajKategorije():
    print("GENERIRANO:")
    kategorije = ['a', 'b', 'c']
    preostaloCvorova = postavke.brojRacunala

    for kat in kategorije:
        nasumicno = random.randint(0, preostaloCvorova)
        preostaloCvorova = preostaloCvorova - nasumicno
        postavke.brojeviPoKat[kat] = nasumicno

        if kat == 'c':
            postavke.brojeviPoKat[kat] += preostaloCvorova

        print(f'Kategorija {kat} = {postavke.brojeviPoKat[kat]}')

def generirajCvorove():
    print("Računala:", end=' ')
    postavke.cvorovi = []
    for kat in postavke.kategorije:
        for br in range(1, postavke.brojeviPoKat[kat]+1):
            noviCvor = kat + str(br)
            postavke.cvorovi.append(noviCvor)
            print(noviCvor, end=' ')
    print()

def izracunajNajkraciPut(G):
    cvoroviNaNajkracem = nx.shortest_path(G, source=postavke.pocetakSirenja, target=postavke.krajSirenja, weight='weight')

    ukupnaTezina = 0
    for i in range(0, len(cvoroviNaNajkracem)-1):
        ukupnaTezina += dohvatiTezinuBrida((cvoroviNaNajkracem[i], cvoroviNaNajkracem[i+1]))

    print("Duljina najkraceg puta = ", ukupnaTezina)
    print('-'.join(map(str, cvoroviNaNajkracem)))
    return cvoroviNaNajkracem

def izracunajDuljinuPuta(put):
    ukupnaTezina = 0
    for i in range(0, len(put) - 1):
        ukupnaTezina += dohvatiTezinuBrida((put[i], put[i+1]))

    return ukupnaTezina

def izracunajHamiltonoveCikluse(G):
    F = [(G, [list(G.nodes())[0]])]
    n = G.number_of_nodes()

    ciklusi = []
    while F:
        graph, path = F.pop()
        confs = []
        susjedi = (node for node in graph.neighbors(path[-1])
                   if node != path[-1])
        for susjed in susjedi:
            conf_p = path[:]
            conf_p.append(susjed)
            conf_g = nx.Graph(graph)
            conf_g.remove_node(path[-1])
            confs.append((conf_g, conf_p))
        for g, p in confs:
            if len(p) == n:
                ciklusi.append(p)
            else:
                F.append((g, p))

    unikatniCiklusi = set(tuple(i) for i in ciklusi)

    if len(unikatniCiklusi) > 0:
        return unikatniCiklusi

    return None

def pronadiNajkraciHamiltonov(G):
    ciklusi = izracunajHamiltonoveCikluse(G)

    najkraciCiklus = []
    najkracaDuljina = 999999
    for ciklus in ciklusi:
        trenDuljina = izracunajDuljinuPuta(ciklus)
        if najkracaDuljina > trenDuljina:
            najkraciCiklus = ciklus
            najkracaDuljina = trenDuljina

    print("Minimalno vrijeme širenja: ", najkracaDuljina)
    print("Put do svih: ", '-'.join(map(str, najkraciCiklus)))

def dohvatiOznaceneBridove(najkraciPut):
    bridovi = []
    for i in range(0, len(najkraciPut)-1):
        bridovi.append((najkraciPut[i], najkraciPut[i+1]))
        bridovi.append((najkraciPut[i+1], najkraciPut[i]))

    return bridovi

def dodajBridove(G):
    for brid in postavke.bridovi:
        tezina = dohvatiTezinuBrida(brid)
        G.add_edge(brid[0], brid[1], weight=tezina)

def iscrtajGraf():
    G = nx.Graph()
    dodajBridove(G)

    values = [0.1 for node in G.nodes()]
    oznakeBridova = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    oznakeCvorova = {node: node for node in G.nodes()}

    crveniBridovi = dohvatiOznaceneBridove(izracunajNajkraciPut(G))
    bojeBridova = ['black' if not edge in crveniBridovi else 'red' for edge in G.edges()]

    pronadiNajkraciHamiltonov(G)

    pos = nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=oznakeBridova)
    nx.draw(G, pos, node_color=values, node_size=2000, edge_color=bojeBridova, edge_cmap=plt.cm.Reds)
    nx.draw_networkx_labels(G, pos, labels=oznakeCvorova)
    plt.show()

dohvatiPostavke()
generirajKategorije()
generirajCvorove()
dohvatiOstatakPostavki()
generirajBridove()
iscrtajGraf()
