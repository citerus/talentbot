import unittest
from envvars import verifyEnvironmentVariablesArgs
from main import getCommands
from command import Command, Help

class StartupTest(unittest.TestCase):
    def test_EmptyTrelloApiKeyReturnsErrorMessage(self):
        emptyApiKey = ""
        result = verifyEnvironmentVariablesArgs(TRELLO_API_KEY=emptyApiKey, b="1", c="2", d="3", e="4")
        self.assertEquals(result, "Environment property TRELLO_API_KEY not set, aborting.")

    def test_EmptySlackTokenReturnsErrorMessage(self):
        result = verifyEnvironmentVariablesArgs(a="1", b="2", c="3", d="4", SLACK_TOKEN=None)
        self.assertEquals(result, "Environment property SLACK_TOKEN not set, aborting.")

    def test_ReturnNoneIfAllEnvVarsAreSet(self):
        result = verifyEnvironmentVariablesArgs(a="1", b="2", c="3", d="4", e="5")
        self.assertEquals(result, None)

    def test_getCommandsShouldInstantiateAndReturnAllCommandSubclasses(self):
        slack = trello = None
        commands = getCommands(slack, trello)
        self.assertTrue(len(commands) > 0)
        filteredList = filter(lambda cls: isinstance(cls, Command), commands)
        self.assertEquals(len(filteredList), len(commands))
        listWithHelp = filter(lambda cls: isinstance(cls, Help), commands)
        self.assertEquals(len(listWithHelp), 1)

def main():
    unittest.main()

if __name__ == '__main__':
    main()