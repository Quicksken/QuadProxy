import json
from fpdf import FPDF


class PDF(FPDF):
    def background(self):
        if cardsPerPage == 9:
            self.rect(paddingWidth, paddingHeight, cardWidth, cardHeight)
            self.rect(paddingWidth + cardWidth, paddingHeight, cardWidth, cardHeight)
            self.rect(paddingWidth + cardWidth * 2, paddingHeight, cardWidth, cardHeight)
            self.rect(paddingWidth, paddingHeight + cardHeight, cardWidth, cardHeight)
            self.rect(paddingWidth + cardWidth, paddingHeight + cardHeight, cardWidth, cardHeight)
            self.rect(paddingWidth + cardWidth * 2, paddingHeight + cardHeight, cardWidth, cardHeight)
            self.rect(paddingWidth, paddingHeight + cardHeight * 2, cardWidth, cardHeight)
            self.rect(paddingWidth + cardWidth, paddingHeight + cardHeight * 2, cardWidth, cardHeight)
            self.rect(paddingWidth + cardWidth * 2, paddingHeight + cardHeight * 2, cardWidth, cardHeight)

    def makePages(self):
        if cardsPerCard == 1:
            self.set_font('dejavu', '', 9)
        for deck in decks:
            for index, card in enumerate(deck.main):
                if index % 9 == 0:
                    pdf.add_page()
                    pdfPages.append(Page(index / 9))
                    pdf.background()
                cP = pdfPages[int(index / 9)]
                cS = cP.slots[index % 9]
                self.set_xy(cS.sX, cS.sY)
                self.cell(cardWidth - 12, 5, card.name, align='L')
                self.cell(10, 5, card.cost, align='R', ln=1)
                self.set_x(cS.sX)
                self.multi_cell(cardWidth - 2, 4, card.text, align='L')
                self.set_xy(cS.sX, cS.sY + cardHeight - 6)
                self.cell(cardWidth - 18, 0, card.typeLine, align='L')
                self.cell(16, 0, card.powTgh, align='R')


class Page:
    def __init__(self, pnr):
        self.pageNr = pnr
        self.pX = paddingWidth
        self.pY = paddingHeight
        self.slotsCnt = cardsPerPage
        self.slots = []
        if cardsPerPage == 9:
            index = 0
            while index < cardsPerPage:
                self.slots.append(Slot(self, index))
                index += 1


class Slot:
    def __init__(self, page, index):
        self.index = index
        self.sX = page.pX + 1
        self.sY = page.pY + 1
        if index == 0:
            pass
        if 0 < index < 3:
            self.sX += cardWidth * (index % 3)
        if 2 < index < 6:
            self.sY += cardHeight
            self.sX += cardWidth * (index % 3)
        if 5 < index < 9:
            self.sY += cardHeight * 2
            self.sX += cardWidth * (index % 3)
        #print(self.sX, self.sY)


#
# class Box:
#     def __init__(self, slotIndex, boxType):
#         self.slotIndex = slotIndex
#         self.boxType = boxType
#         if slotIndex = 0:
#

class Deck:
    def __init__(self, name, main, side=None):
        if side is None:
            side = []
        self.name = name
        self.main = main
        self.side = side
        self.length = len(main)
        if side is not None:
            self.length += len(side)


class Card:
    def __init__(self, name=''):
        self.name = name
        try:
            cost = cardjson['manaCost']
            braces = ['{', '}']
            for brace in braces:
                cost = cost.replace(brace, '')
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


def countPages():
    deckLengths = []
    for deck in decks:
        deckLengths.append(deck.length)
    deckLengths.sort()
    if deckLengths[-1] % cardsPerPage != 0:
        return deckLengths[-1] / 9 + 1
    else:
        return deckLengths[-1] / 9


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
    # initialise JSON object
    f = open('AtomicCards.json', 'r', encoding='utf-8')
    mtgjson = json.loads(f.read())

    # make Deck object(s)
    d = 0
    decks = []
    while d < len(decklists):  # grab each decklist and split it into a list of amounts and cards
        mainList = []
        for x in decklists[d][1].splitlines():
            mainList.extend(x.split(' ', 1))
        mainCards = []
        i = 0
        while i < len(mainList):  # make Card objects based on the amounts and cards (strings) in mainList,
            # store them in a list mainCards
            cnt = mainList[i]
            i += 1
            j = 0
            while j < int(cnt):
                cardjson = mtgjson['data'][mainList[i]][0]
                mainCards.append(Card(cardjson['name']))
                j += 1
            i += 1
        decks.append(
            Deck(decklists[d][0], mainCards))  # actually make the Deck object with the Card object list mainCards
        d += 1

    # make the PDF
    cardsPerCard = 1
    pdfWidth = 210
    pdfHeight = 297
    cardWidth = 63.5
    cardHeight = 88.9
    pdfFormat = 'A4'
    pdf = PDF(orientation='P', unit='mm', format=pdfFormat)
    pdf.add_font('dejavu', '', 'fonts/DejaVuSans-ExtraLight.ttf', True)
    pdf.add_font('bellgothic', '', 'fonts/ufonts.com_bell-gothic-light.ttf', True)
    if pdfFormat == 'A4':
        cardsPerPage = 9
        paddingWidth = (pdfWidth - (3 * cardWidth)) / 2
        paddingHeight = (pdfHeight - (3 * cardHeight)) / 2
    pageCount = countPages()
    pdfPages = []
    pdf.makePages()
    pdf.output('test.pdf', 'F')
