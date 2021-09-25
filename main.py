import json


class Deck:
    def __init__(self, name, main, side=None):
        if side is None:
            side = []
        self.name = name
        self.main = main
        self.side = side


class Card:
    def __init__(self, name='', cost='', typeLine='', text='', powTgh=''):
        self.name = name
        try:
            cost = cardjson['manaCost']
            self.cost = cost
        except KeyError:
            self.cost = ''
        try:
            typeLine = cardjson['type']
            self.typeLine = typeLine
        except KeyError:
            self.typeLine = ''
        try:
            text = cardjson['text']
            self.text = text
        except KeyError:
            self.text = ''
        try:
            powTgh = cardjson['power'] + '/' + cardjson['toughness']
            self.powTgh = powTgh
        except KeyError:
            self.powTgh = ''
    def printCard(self):
        print(self.name, ' ', self.cost, '\n', self.typeLine, '\n', self.text, '\n', self.powTgh)


decklistName1 = """4c Xan"""

decklist1 = """1 Xanathar, Guild Kingpin
4 Path to the Festival
4 Binding the Old Gods
2 Crush the Weak
4 Sarulf's Packmate
3 Eureka Moment
4 Behold the Multiverse
4 Infernal Grasp
4 Negate
2 Ice Tunnel
2 Rimewood Falls
2 Woodland Chasm
4 Evolving Wilds
2 Snow-Covered Mountain
3 Snow-Covered Swamp
4 Snow-Covered Island
4 Snow-Covered Forest
2 Volatile Fjord
2 Narfi, Betrayer King
1 Koma, Cosmos Serpent
1 Old Gnawbone
1 Orcus, Prince of Undeath
"""

decklistName2 = """UW Delver"""

decklist2 = """4 Clever Lumimancer
4 Delver of Secrets // Insectile Aberration
3 Monk of the Open Hand
1 Poppet Stitcher // Poppet Factory
1 Monk Class
4 Curate
4 Flare of Faith
2 Fading Hope
4 Consider
2 Show of Confidence
1 Fateful Absence
9 Plains
9 Island
4 Evolving Wilds
4 Guiding Voice
3 Homestead Courage
1 Hallowed Respite
"""
deckCount = 2

decklists = [[decklistName1, decklist1], [decklistName2, decklist2]]

if __name__ == "__main__":
    f = open('AtomicCards.json', 'r', encoding='utf-8')
    mtgjson = json.loads(f.read())
    # print(mtgjson['data']['Black Lotus'][0]['text'])
    # turn text into qty+name lists
    d = 0
    decks = []
    while d < len(decklists):
        mainList = []
        for x in decklists[d][1].splitlines():
            mainList.extend(x.split(' ', 1))
        mainCards = []
        i = 0
        while i < len(mainList):
            cnt = mainList[i]
            i += 1
            j = 0
            while j < int(cnt):
                cardjson = mtgjson['data'][mainList[i]][0]
                mainCards.append(Card(cardjson['name']))
                j += 1
            i += 1
        decks.append(Deck(decklists[d][0], mainCards))
        d += 1



