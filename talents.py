from trello import TrelloClient

TRELLO_BOARD_ID = 'hud22dPi'

class TrelloTalents:
    
    def __init__(self, api_key, api_secret, token, token_secret):
        self.client = TrelloClient(api_key, api_secret, token, token_secret)

    def talentBoard(self):
        return self.client.get_board(TRELLO_BOARD_ID)
    
    def getTalentsByEmail(self, emailAddr):
        users_talent_list = [l for l in self.talentBoard().get_lists('open') if l.name == emailAddr][0]
        users_talent_cards = [card.name for card in users_talent_list.list_cards()]
        return self.convertListToUtf8String(users_talent_cards)

    def getPersonEmailsByTalent(self, talentName):
        return [l.name for l in self.talentBoard().get_lists('open') if len([c for c in l.list_cards() if talentName.lower() == c.name.decode('utf-8').lower()]) > 0]
    
    def convertListToUtf8String(self, list):
        return str('\n- ' + '\n- '.join(list)).decode('utf-8')
