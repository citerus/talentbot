import unittest
import os
from talents import TrelloTalents
from trello import TrelloClient

'''
These tests call out via the TrelloClient wrapper
and expect a testing list to be available on the board,
filled with cards named after the words in the NATO
phonetic alphabet.
'''
class TrelloTest(unittest.TestCase):
    
    # A talent that is virtually guaranteed to exist on
    # the board on more than one person's lists.
    COMMON_TALENT = "Scrum"
    
    def setUp(self):
        self.api_key         = os.environ['TRELLO_API_KEY']
        self.api_secret      = os.environ['TRELLO_API_SECRET']
        self.token           = os.environ['TRELLO_TOKEN']
        self.token_secret    = os.environ['TRELLO_TOKEN_SECRET']
        tc = TrelloClient(self.api_key, self.api_secret, self.token, self.token_secret)
        self.tt = TrelloTalents(tc)
    
    def test_created(self):
        self.assertIsNotNone(self.tt)
        
    def test_board_name(self):
        board = self.tt.talentBoard()
        self.assertEqual("Talanger", board.name)
        
    def test_fetch_talents(self):
        email = "test.test@citerus.se"
        trelloData = self.tt.getTalentsByEmailAsList(email)
        self.assertEqual(26, len(trelloData))
        self.assertEqual("Alpha", trelloData[0])
        self.assertEqual("Zulu", trelloData[-1])
        
    def test_fetch_single_match(self):
        talent = "Juliett"
        emails = self.tt.getPersonEmailsByTalent(talent)
        self.assertEqual(1, len(emails))
        self.assertEqual("test.test@citerus.se", emails[0])
        
    def test_fetch_multiple_matches(self):
        talent = self.COMMON_TALENT
        emails = self.tt.getPersonEmailsByTalent(talent)
        self.assertTrue(len(emails) > 1)
        self.assertIn("tobias.fors@citerus.se", emails)
        
    def test_fetch_all_talents(self):
        talents = self.tt.getAllTalents()
        self.assertTrue(len(talents) > 1)
        self.assertIn("Alpha", talents)
        self.assertIn(self.COMMON_TALENT, talents)
        self.assertIn("Zulu", talents)    
        
suite = unittest.TestLoader().loadTestsFromTestCase(TrelloTest)
unittest.TextTestRunner(verbosity=2).run(suite)

# suite = unittest.TestSuite()
# suite.addTest(TrelloTest("test_fetch_all_talents"))
# runner = unittest.TextTestRunner()
# runner.run(suite)
