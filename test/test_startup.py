import unittest
from envvars import verifyEnvironmentVariablesArgs

class StartupTest(unittest.TestCase):
    def testEmptyTrelloApiKeyReturnsErrorMessage(self):
        emptyApiKey = ""
        result = verifyEnvironmentVariablesArgs(TRELLO_API_KEY=emptyApiKey, b="1", c="2", d="3", e="4")
        self.assertEquals(result, "Environment property TRELLO_API_KEY not set, aborting.")

    def testEmptySlackTokenReturnsErrorMessage(self):
        result = verifyEnvironmentVariablesArgs(a="1", b="2", c="3", d="4", SLACK_TOKEN=None)
        self.assertEquals(result, "Environment property SLACK_TOKEN not set, aborting.")

    def testReturnNoneIfAllEnvVarsAreSet(self):
        result = verifyEnvironmentVariablesArgs(a="1", b="2", c="3", d="4", e="5")
        self.assertEquals(result, None)

def main():
    unittest.main()

if __name__ == '__main__':
    main()