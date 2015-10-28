import unittest
from main import verifyEnvironmentVariables

class StartupTest(unittest.TestCase):
    def testEmptyTrelloApiKeyReturnsErrorMessage(self):
        emptyApiKey = ""
        result = verifyEnvironmentVariables(emptyApiKey, "", "", "", "")
        self.assertEquals(result, "Environment property TRELLO_API_KEY not set, aborting.")

    def testEmptySlackTokenReturnsErrorMessage(self):
        result = verifyEnvironmentVariables("1", "2", "3", "4", None)
        self.assertEquals(result, "Environment property SLACK_TOKEN not set, aborting.")

    def testReturnNoneIfAllEnvVarsAreSet(self):
        result = verifyEnvironmentVariables("1", "2", "3", "4", "5")
        self.assertEquals(result, None)

def main():
    unittest.main()

if __name__ == '__main__':
    main()