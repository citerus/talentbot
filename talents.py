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
    
    def getTalentsByEmailAsList(self, emailAddr):
        users_talent_list = [l for l in self.talentBoard().get_lists('open') if l.name == emailAddr][0]
        users_talent_cards = [card.name for card in users_talent_list.list_cards()]
        return users_talent_cards

    def getPersonEmailsByTalent(self, talentName):
        listLengthFn = lambda c: len([c for c in l.list_cards() if talentName.lower() == c.name.decode('utf-8').lower()]) > 0
        return [l.name for l in self.talentBoard().get_lists('open') if listLengthFn]
    
    def getPersonEmailsByTalent2(self, talentName):
        # We're working with the TrelloClient wrapper here,
        # so the lists and the cards are types defined by TrelloClient
        all_lists = self.talentBoard().open_lists()
        
        lists_containing_talent = []
        
        for l in all_lists:
            for c in l.list_cards():
                if self.is_match(c, talentName):
                    lists_containing_talent.append(l)
        
        return [match.name for match in lists_containing_talent]
    
    def getAllTalents(self):
        all_cards = self.talentBoard().all_cards()        
        unique_cards = list(set([card.name for card in flatten(all_cards)]))
        return convertListToUtf8String(unique_cards)
        
    @staticmethod
    def is_match(card, talent_name):
        return card.name.decode('utf-8').lower() == talent_name.lower()

def convertListToUtf8String(strList):
    return '' if len(strList) == 0 else str('\n- ' + '\n- '.join(strList)).decode('utf-8')
