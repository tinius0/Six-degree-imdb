
class Skuespiller:
    def __init__(self, nm_id : str, navn : str):
        self.nm_id = nm_id
        self.navn = navn
        self.filmer = []

    def legg_til_film(self, film):
        self.filmer.append(film)

    def hent_navn(self):
        return self.navn
    
    def hent_nmid(self):
        return self.nm_id

class Film:
    def __init__(self, tt_id, tittel, rating):
        self.tt_id = tt_id
        self.tittel = tittel
        self.rating = rating
        self.skuespillere = []

    def legg_til_skuespiller(self, skuepiller : Skuespiller):
        self.skuespillere.append(skuepiller)

    def hent_skuespillere(self):
        return self.skuespillere
    
    def hent_tittel(self):
        return self.tittel
    
    def hent_rating(self):
        return self.rating

class Graph:
    def __init__(self):
        self.kanter = dict() #kanter[nm_id1] = [[nm_id1 : str, nm_id2 : str, film : Film]]
        self.skuespillere = dict() #skuespillere[navn_id] = skuespiller_obj
        self.filmer = dict() #filmer[film_id] = film_obj
        self.ant_noder = 0
        self.ant_kanter = 0

    def ny_node(self, nm_id : str, skuespiller : Skuespiller):
        self.kanter[nm_id] = []
        self.skuespillere[nm_id] = skuespiller
        self.ant_noder += 1

    def ny_kant(self, nm_id : str, nm_id2 : str, film:Film):
        self.kanter[nm_id].append([nm_id, nm_id2, film])
        self.kanter[nm_id2].append([nm_id2, nm_id, film])
        self.ant_kanter += 1

    def hent_ant_noder(self):
        return self.ant_noder

    def hent_ant_kanter(self):
        return self.ant_kanter

    def hent_graf_dict(self):
        return self.kanter
    

    def lag_graf(self, filmfil, skuespillerfil):

        with open(filmfil, 'r', encoding = 'utf-8') as fil:
            for linje in fil:
                film = linje.strip().split("\t")
                obj = Film(film[0], film[1], film[2])
                self.filmer[film[0]] = obj
            
        with open(skuespillerfil, 'r', encoding = 'utf-8') as fil:
            for linje in fil:
                info = linje.strip().split("\t")
                skuespiller = Skuespiller(info[0], info[1])
                filmer = info[2:]
                self.ny_node(info[0], skuespiller)
                for film in filmer:
                    if film in self.filmer.keys():
                        self.filmer[film].legg_til_skuespiller(skuespiller)

        for film in self.filmer.keys():
            skuespillere = self.filmer[film].hent_skuespillere()
            for i in range(len(skuespillere)):
                for j in range(i+1, len(skuespillere)):
                    self.ny_kant(skuespillere[i].hent_nmid(), skuespillere[j].hent_nmid(), self.filmer[film])


    def bredde_foerst(self, start, slutt):
        besoekt = dict() #besoekt[besoekt_node] = [kanter]

        #lage en ordbok, hvor hver nøkkel er en node og verdi er kantene som ble brukt for å komme dit fra start
        besoekt[start] = []
        
        kø = [start]

        while kø:
            node = kø.pop(0)
            for i in range(len(self.kanter[node])):
                nabo = self.kanter[node][i][1]

                if nabo not in besoekt: #self.kanter[kant][i][1]  = nameid
                    kø.append(nabo)
                    besoekt[nabo] = besoekt[node] + [self.kanter[node][i]]
                    #besoekt[kant] liste med kanter fra start til kant
                    #legger til i lista, kanten fra kant til nmid

                    if nabo == slutt:
                        return besoekt[slutt]


    def skriv_ut_sti(self, liste):
        utskrift = self.skuespillere[liste[0][0]].hent_navn() + "\n"

        for i in range(len(liste)):
            utskrift += f'=== [ {liste[i][2].hent_tittel()} ({liste[i][2].hent_rating()}) ] ===> {self.skuespillere[liste[i][1]].hent_navn()}\n'

        return utskrift

def main():
    graf = Graph()
    graf.lag_graf("movies.tsv", "actors.tsv")
    print(f'antall noder: {graf.hent_ant_noder()}')
    print(f'antall kanter: {graf.hent_ant_kanter()}')


    oppgave = [["nm2255973", "nm0000460"], ["nm0424060" , "nm8076281"], ["nm4689420","nm0000365"], ["nm0000288", "nm2143282"], ["nm0637259","nm0931324"]]
    for i in range(len(oppgave)):
        print(graf.skriv_ut_sti(graf.bredde_foerst(oppgave[i][0], oppgave[i][1])))

if __name__ == '__main__':
    main()


    
    