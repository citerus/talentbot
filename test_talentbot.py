import unittest
import json
from talentbot import SlackEvent

class SlackEventTest(unittest.TestCase):
    def testCanIdentifyMessage(self):
        event = messageWithText("hej")
        self.assertTrue(event.isMessage())

    def testCanIdentifySingleKeyword(self):
        event = messageWithText("banana")
        self.assertTrue(event.textContainsKeyword("banana"))

    def testCanIdentifyKeywordFollowedByArgument(self):
        event = messageWithText("banana split")
        self.assertTrue(event.textContainsKeyword("banana"))

def messageWithText(text):
    event = {}
    event['type'] = 'message'
    event['text'] = text
    return SlackEvent(json.loads(json.dumps(event)))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
