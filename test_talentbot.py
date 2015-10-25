import unittest
import json
from talentbot import SlackEvent

class SlackEventTest(unittest.TestCase):
    def testCanIdentifySingleKeyword(self):
        event = eventWithText("banana")
        self.assertTrue(event.textContainsKeyword("banana"))

    def testCanIdentifyKeywordFollowedByArgument(self):
        event = eventWithText("banana split")
        self.assertTrue(event.textContainsKeyword("banana"))

def eventWithText(text):
    jsonString = '{"text" : "' + text + '"}'
    eventJson = json.loads(jsonString)
    return SlackEvent(eventJson)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
