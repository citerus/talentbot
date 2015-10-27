from trello import TrelloClient
from itertools import chain as flatten

TRELLO_BOARD_ID = 'hud22dPi'

class TrelloTalents:
    
    def __init__(self, trello_client):
        self.client = trello_client

    def talentBoard(self):
        return self.client.get_board(TRELLO_BOARD_ID)
    
    def getTalentsByEmail(self, emailAddr):
        users_talent_list = [l for l in self.talentBoard().get_lists('open') if l.name == emailAddr][0]
        users_talent_cards = [card.name for card in users_talent_list.list_cards()]
        return convertListToUtf8String(users_talent_cards)

    def getPersonEmailsByTalent(self, talentName):
        listLengthFn = lambda c: len([c for c in l.list_cards() if talentName.lower() == c.name.decode('utf-8').lower()]) > 0
        return [l.name for l in self.talentBoard().get_lists('open') if listLengthFn]

    def getAllTalents(self):
        lists = [l.list_cards() for l in self.talentBoard().get_lists('open')]
        cards = list(set([card.name for card in flatten(lists)]))
        return convertListToUtf8String(cards)

def convertListToUtf8String(strList):
    return str('\n- ' + '\n- '.join(strList)).decode('utf-8')
