import unittest
import os
from talents import TrelloTalents
from trello import TrelloClient

class TrelloTest(unittest.TestCase):
    def setUp(self):
        self.api_key         = os.environ['TRELLO_API_KEY']
        self.api_secret      = os.environ['TRELLO_API_SECRET']
        self.token           = os.environ['TRELLO_TOKEN']
        self.token_secret    = os.environ['TRELLO_TOKEN_SECRET']
        tc = TrelloClient(self.api_key, self.api_secret, self.token, self.token_secret)
        self.tt = TrelloTalents(tc)
    
    def test_create(self):
        self.assertIsNotNone(self.tt)
        
    def test_fetch(self):
        email = "tobias.fors@citerus.se"
        trelloData = self.tt.getTalentsByEmail(email)
        print trelloData

suite = unittest.TestLoader().loadTestsFromTestCase(TrelloTest)
unittest.TextTestRunner(verbosity=2).run(suite)